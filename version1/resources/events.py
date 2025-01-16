from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import EventSchema, EventUpdateSchema
from models.event import EventModel
from db import db
from datetime import datetime

blp = Blueprint("Events", __name__, description="Operations on events")


@blp.route("/event")
class EventList(MethodView):
    @blp.response(200, EventSchema(many=True))
    def get(self):
         return list(db.get("events", {}).values())
    @blp.arguments(EventSchema)
    @blp.response(201, EventSchema)
    def post(self, new_event):
        try:
            event_id = max(event.id for event in db.get("events", {}).values()) + 1
        except ValueError:
            event_id = 1
        film_name = db.get("films", {}).get(new_event["film_id"]).title
        film_duration = db.get("films", {}).get(new_event["film_id"]).duration
        venue_name = db.get("venues", {}).get(new_event["venue_id"]).name

        event = EventModel(id=event_id,
                           film_id=new_event["film_id"],
                           film_name=film_name,
                           film_duration=film_duration,
                           venue_id=new_event["venue_id"],
                           venue_name=venue_name,
                           date=new_event["date"],
                           start_time=new_event["start_time"])
        if "events" not in db:
            db["events"] = {}
        db["events"][event_id] = event
        return event

@blp.route("/event/<int:event_id>")
class EventById(MethodView):
    @blp.response(200, EventSchema)
    def get(self, event_id):
        try:
            return db["events"][event_id]
        except KeyError:
           abort(404, message="Event not found")
    @blp.arguments(EventUpdateSchema)
    @blp.response(200, EventSchema)
    def put(self, updated_event, event_id):
        try:
             event = db["events"][event_id]
             for key, value in updated_event.items():
                 setattr(event, key, value)
             return event
        except KeyError:
            abort(404, message="Event not found")
    def delete(self, event_id):
        try:
           del db["events"][event_id]
           return {"message": "Event deleted."}
        except KeyError:
            abort(404, message="Event not found")

@blp.route("/event/date/<string:date>")
class EventByDate(MethodView):
    @blp.response(200, EventSchema(many=True))
    def get(self, date):
        events = db.get("events", {}).values()
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        filtered_events = [event for event in events if event.date == parsed_date]
        return filtered_events

@blp.route("/event/film/<int:film_id>")
class EventByFilm(MethodView):
    @blp.response(200, EventSchema(many=True))
    def get(self, film_id):
        events=db.get("events", {}).values()
        filtered_events=[event for event in events if event.film_id == film_id]
        return filtered_events