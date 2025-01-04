import uuid
from flask import Blueprint, request, jsonify, abort
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.event import EventModel
from schemas import EventSchema
from db import db

blp = Blueprint("Events", "events", description="Operations on events")

@blp.route("/events")
class EventList(MethodView):
    @blp.response(200, EventSchema(many=True))
    def get(self):
        """Get all events"""
        return EventModel.query.all()

    @blp.arguments(EventSchema)
    @blp.response(201, EventSchema)
    def post(self, event_data):
        """Create a new event"""
        event_data['id'] = uuid.uuid4()
        event = EventModel(**event_data)
        try:
            db.session.add(event)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An event with that details already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the event.")
        return event

@blp.route("/event/<int:event_id>")
class Event(MethodView):
    @blp.response(200, EventSchema)
    def get(self, event_id):
        """Get an event by ID"""
        event = EventModel.query.get_or_404(event_id)
        return event

    @blp.arguments(EventSchema)
    @blp.response(200, EventSchema)
    def put(self, event_data, event_id):
        """Update an event by ID"""
        event = EventModel.query.get_or_404(event_id)
        
        # Update the event with the new data
        for key, value in event_data.items():
            setattr(event, key, value)
        
        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred updating the event.")
        return event

    @blp.response(204)
    def delete(self, event_id):
        """Delete an event by ID"""
        event = EventModel.query.get_or_404(event_id)
        try:
            db.session.delete(event)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred deleting the event.")
        return "", 204

@blp.route("/events/date/<string:date>")
class EventsByDate(MethodView):
    @blp.response(200, EventSchema(many=True))
    def get(self, date):
        """Get events by date"""
        events = EventModel.query.filter_by(date=date).all()
        return events

@blp.route("/events/film/<int:film_id>")
class EventsByFilm(MethodView):
    @blp.response(200, EventSchema(many=True))
    def get(self, film_id):
        """Get events by film"""
        events = EventModel.query.filter_by(film_id=film_id).all()
        return events