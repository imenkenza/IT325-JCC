from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models import User, Film, Venue, Event, Schedule

class UserSchema(SQLAlchemySchema):
  class Meta:
    model = User
    load_instance = True

  id = auto_field(dump_only=True)
  username = auto_field(required=True)
  email = auto_field(required=True)
  password = auto_field(required=True, load_only=True)
  created_at = auto_field(dump_only=True)

class FilmSchema(SQLAlchemySchema):
    class Meta:
        model = Film
        load_instance = True

    id = auto_field(dump_only=True)
    title = auto_field(required=True)
    category = auto_field(required=True)
    genre = auto_field(required=True)
    country = auto_field(required=True)
    duration = auto_field(required=True)
    description = auto_field()
    created_at = auto_field(dump_only=True)

class VenueSchema(SQLAlchemySchema):
  class Meta:
    model = Venue
    load_instance = True

  id = auto_field(dump_only=True)
  name = auto_field(required=True)
  created_at = auto_field(dump_only=True)

class EventSchema(SQLAlchemySchema):
  class Meta:
    model = Event
    load_instance = True

  id = auto_field(dump_only=True)
  film_id = auto_field(required=True)
  venue_id = auto_field(required=True)
  date = auto_field(required=True)
  start_time = auto_field(required=True)
  created_at = auto_field(dump_only=True)

class ScheduleSchema(SQLAlchemySchema):
    class Meta:
        model = Schedule
        load_instance = True

    id = auto_field(dump_only=True)
    user_id = auto_field(required=True)
    event_id = auto_field(required=True)
    created_at = auto_field(dump_only=True)