from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, URL, Optional

class URLForm(FlaskForm):
    original_url = StringField('Original URL', validators=[DataRequired(), URL()])
    custom_token = StringField('Custom Token', validators=[Optional()])
    expiration_date = DateField('Expiration Date', validators=[Optional()])
    submit = SubmitField('Shorten URL')
