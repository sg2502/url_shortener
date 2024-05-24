from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

from models import URL


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        custom_token = request.form.get('custom_token')
        expiration_date = request.form.get('expiration_date')
        if not custom_token:
            custom_token = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if expiration_date:
            expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
        else:
            expiration_date = datetime.now() + timedelta(days=30)

        new_url = URL(original_url=original_url, short_url=custom_token, expiration_date=expiration_date)
        db.session.add(new_url)
        db.session.commit()
        return render_template('short_url.html', short_url=custom_token)

    return render_template('index.html')


@app.route('/<short_url>')
def redirect_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    if url.expiration_date >= datetime.now():
        url.clicks += 1
        db.session.commit()
        return redirect(url.original_url)
    else:
        flash('The URL has expired.')
        return redirect(url_for('index'))


@app.route('/analytics/<short_url>')
def analytics(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    return render_template('analytics.html', url=url)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
