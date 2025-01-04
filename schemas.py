from marshmallow import Schema, fields

class FilmSchema(Schema):
    id = fields.UUID(dump_only=True)
    title = fields.Str(required=True)
    director = fields.Str(required=True)
    release_date = fields.Date(required=True)
    genre = fields.Str(required=True)

class VenueSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    capacity = fields.Int(required=True)

class EventSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    date = fields.DateTime(required=True)
    venue_id = fields.UUID(required=True)
    film_id = fields.UUID(required=True)