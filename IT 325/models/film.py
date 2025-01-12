from db import db
from datetime import datetime

class Film(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  category = db.Column(db.String(100), nullable=False)
  genre = db.Column(db.String(100), nullable=False)
  country = db.Column(db.String(100), nullable=False)
  duration = db.Column(db.Integer, nullable=False)
  description = db.Column(db.Text, nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  events = db.relationship('Event', backref='film', lazy=True)

  def __init__(self, title, category, genre, country, duration, description):
    self.title = title
    self.category = category
    self.genre = genre
    self.country = country
    self.duration = duration
    self.description = description

  def __repr__(self):
        return f'<Film {self.title}>'