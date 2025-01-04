from db import db

class VenueModel(db.Model):
    __tablename__ = "venues"  # Ensure this matches the foreign key reference
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    # Relationship to EventModel
    events = db.relationship("EventModel", back_populates="venue")