from app import db
from datetime import datetime

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    short_url = db.Column(db.String(6), unique=True, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    clicks = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<URL {self.short_url}>'
