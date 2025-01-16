from marshmallow import Schema, fields

class FilmSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    category = fields.Str(required=True)
    genre = fields.Str(required=True)
    country = fields.Str(required=True)
    duration = fields.Int(required=True)
    description = fields.Str()

class VenueSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    film_id = fields.Int(required=True)
    film_name = fields.Str(dump_only=True)
    film_duration = fields.Int(dump_only=True)
    venue_id = fields.Int(required=True)
    venue_name = fields.Str(dump_only=True)
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)

class EventUpdateSchema(Schema):
    date = fields.Date()
    start_time = fields.Time()