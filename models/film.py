from db import db

class FilmModel(db.Model):
    __tablename__ = "films"  
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    # Relationship to EventModel
    events = db.relationship("EventModel", back_populates="film")