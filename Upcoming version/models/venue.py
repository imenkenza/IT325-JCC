from db import db
from datetime import datetime

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    events = db.relationship('Event', backref='venue', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
      return f'<Venue {self.name}>'