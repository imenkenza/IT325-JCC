from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import VenueSchema
from models.venue import VenueModel
from db import db

blp = Blueprint("Venues", __name__, description="Operations on venues")


@blp.route("/venue")
class VenueList(MethodView):
    @blp.response(200, VenueSchema(many=True))
    def get(self):
        return list(db.get("venues", {}).values())

    @blp.arguments(VenueSchema)
    @blp.response(201, VenueSchema)
    def post(self, new_venue):
        try:
            venue_id = max(venue.id for venue in db.get("venues", {}).values()) + 1
        except ValueError:
            venue_id = 1
        venue = VenueModel(id=venue_id, **new_venue)
        if "venues" not in db:
            db["venues"] = {}
        db["venues"][venue_id] = venue
        return venue

@blp.route("/venue/<int:venue_id>")
class VenueById(MethodView):
    @blp.response(200, VenueSchema)
    def get(self, venue_id):
        try:
            return db["venues"][venue_id]
        except KeyError:
            abort(404, message="Venue not found")

    @blp.arguments(VenueSchema)
    @blp.response(200, VenueSchema)
    def put(self, updated_venue, venue_id):
        try:
            venue= db["venues"][venue_id]
            for key, value in updated_venue.items():
                setattr(venue,key,value)
            return venue
        except KeyError:
            abort(404, message="Venue not found")

    def delete(self, venue_id):
        try:
             del db["venues"][venue_id]
             return {"message": "Venue deleted."}
        except KeyError:
             abort(404, message="Venue not found")