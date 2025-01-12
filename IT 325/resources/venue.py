from flask import request, jsonify
from db import db
from models import Venue
from schemas import VenueSchema
from flask_jwt_extended import jwt_required

from db import create_app

app = create_app()

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)

@app.route('/venues', methods=['GET'])
@jwt_required()
def get_all_venues():
    venues = Venue.query.all()
    result = venues_schema.dump(venues)
    return jsonify(result), 200

@app.route('/venues', methods=['POST'])
@jwt_required()
def post_venue():
  data = request.get_json()
  if not data:
      return {'message': "Invalid data"}, 400
  venue = venue_schema.load(data)
  db.session.add(venue)
  db.session.commit()
  return venue_schema.dump(venue), 201

@app.route('/venues/<int:id>', methods=['PUT'])
@jwt_required()
def put_venue(id):
    venue = Venue.query.get(id)
    if not venue:
      return {'message': 'Venue not found'}, 404
    data = request.get_json()
    if not data:
        return {'message': "Invalid data"}, 400
    updated_venue = venue_schema.load(data, instance=venue)
    db.session.commit()
    return venue_schema.dump(updated_venue), 200

@app.route('/venues/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_venue(id):
    venue = Venue.query.get(id)
    if venue:
        db.session.delete(venue)
        db.session.commit()
        return {'message': 'Venue deleted'}, 200
    else:
        return {'message': 'Venue not found'}, 404

if __name__ == '__main__':
  app.run(debug=True)