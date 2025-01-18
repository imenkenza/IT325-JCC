from flask import request, jsonify
from db import db
from models import Event
from schemas import EventSchema
from flask_jwt_extended import jwt_required
from datetime import datetime
from sqlalchemy import or_
from db import create_app

app = create_app()

event_schema = EventSchema()
events_schema = EventSchema(many=True)

@app.route('/events', methods=['GET'])
@jwt_required()
def get_all_events():
    events = Event.query.all()
    result = events_schema.dump(events)
    return jsonify(result), 200

@app.route('/events/<int:id>', methods=['GET'])
@jwt_required()
def get_event_by_id(id):
    event = Event.query.get(id)
    if event:
        result = event_schema.dump(event)
        return jsonify(result), 200
    else:
        return {'message': 'Event not found'}, 404

@app.route('/events/date/<string:date>', methods=['GET'])
@jwt_required()
def get_events_by_date(date):
  try:
      date_obj = datetime.strptime(date, '%Y-%m-%d').date()
  except ValueError:
      return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400
  events = Event.query.filter(Event.date == date_obj).all()
  result = events_schema.dump(events)
  return jsonify(result), 200

@app.route('/events/film/<int:film_id>', methods=['GET'])
@jwt_required()
def get_events_by_film(film_id):
    events = Event.query.filter(Event.film_id == film_id).all()
    result = events_schema.dump(events)
    return jsonify(result), 200

@app.route('/events', methods=['POST'])
@jwt_required()
def post_event():
  data = request.get_json()
  if not data:
      return {'message': "Invalid data"}, 400
  event = event_schema.load(data)
  db.session.add(event)
  db.session.commit()
  return event_schema.dump(event), 201

@app.route('/events/<int:id>', methods=['PUT'])
@jwt_required()
def put_event(id):
  event = Event.query.get(id)
  if not event:
    return {'message': 'Event not found'}, 404
  data = request.get_json()
  if not data:
      return {'message': "Invalid data"}, 400
  updated_event = event_schema.load(data, instance=event)
  db.session.commit()
  return event_schema.dump(updated_event), 200

@app.route('/events/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_event(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return {'message': 'Event deleted'}, 200
    else:
        return {'message': 'Event not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)