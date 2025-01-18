from db import db
from datetime import datetime

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    schedules = db.relationship('Schedule', backref='event', lazy=True)

    def __init__(self, film_id, venue_id, date, start_time):
        self.film_id = film_id
        self.venue_id = venue_id
        self.date = date
        self.start_time = start_time

    def __repr__(self):
        return f'<Event {self.film_id} at {self.venue_id} on {self.date} {self.start_time}>'