from datetime import time
from db import db
from .film import FilmModel
from .venue import VenueModel

class EventModel(db.Model):
    __tablename__ = "events"  
    event_id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.film_id'), nullable=False)
    film_name = db.Column(db.String(100), nullable=False)
    film_duration = db.Column(db.Integer, nullable=False)
    film_category = db.Column(db.String(50), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id'), nullable=False)
    venue_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)

    film = db.relationship("FilmModel", back_populates="events")
    venue = db.relationship("VenueModel", back_populates="events")

    def __init__(self, event_id, venue_id, film_id, date, start_time):
        self.event_id = event_id
        self.venue_id = venue_id
        venue = VenueModel.query.get(venue_id)
        self.venue_name = venue.name
        self.film_id = film_id
        film = FilmModel.query.get(film_id)
        self.film_name = film.title
        self.film_duration = film.duration
        self.film_category = film.category
        self.date = date
        self.start_time = start_time