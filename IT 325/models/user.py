from db import db
from datetime import datetime

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  schedules = db.relationship('Schedule', backref='user', lazy=True)

  def __init__(self, username, email, password):
      self.username = username
      self.email = email
      self.password = password

  def __repr__(self):
    return '<User %r>' % self.username