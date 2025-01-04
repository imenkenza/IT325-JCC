from flask import Blueprint, abort
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.venue import VenueModel
from schemas import VenueSchema
from db import db

blp = Blueprint("Venues", "venues", description="Operations on venues")

@blp.route("/venues")
class VenueList(MethodView):
    @blp.response(200, VenueSchema(many=True))
    def get(self):
        """Get all venues"""
        return VenueModel.query.all()

    @blp.arguments(VenueSchema)
    @blp.response(201, VenueSchema)
    def post(self, venue_data):
        """Create a new venue"""
        venue_data['id'] = uuid.uuid4()
        venue = VenueModel(**venue_data)
        try:
            db.session.add(venue)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A venue with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the venue.")
        return venue

@blp.route("/venue/<int:venue_id>")
class Venue(MethodView):
    @blp.response(200, VenueSchema)
    def get(self, venue_id):
        """Get a venue by ID"""
        venue = VenueModel.query.get_or_404(venue_id)
        return venue

    @blp.arguments(VenueSchema)
    @blp.response(200, VenueSchema)
    def put(self, venue_data, venue_id):
        """Update a venue by ID"""
        venue = VenueModel.query.get_or_404(venue_id)
        
        # Update the venue with the new data
        for key, value in venue_data.items():
            setattr(venue, key, value)
        
        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred updating the venue.")
        return venue

    @blp.response(204)
    def delete(self, venue_id):
        """Delete a venue by ID"""
        venue = VenueModel.query.get_or_404(venue_id)
        try:
            db.session.delete(venue)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred deleting the venue.")
        return "", 204