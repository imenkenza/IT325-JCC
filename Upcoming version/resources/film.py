from flask import request, jsonify
from db import db
from models import Film
from schemas import FilmSchema
from flask_jwt_extended import jwt_required

from db import create_app

app = create_app()

film_schema = FilmSchema()
films_schema = FilmSchema(many=True)

@app.route('/films', methods=['GET'])
@jwt_required()
def get_all_films():
    films = Film.query.all()
    result = films_schema.dump(films)
    return jsonify(result), 200

@app.route('/films/<int:id>', methods=['GET'])
@jwt_required()
def get_film_by_id(id):
    film = Film.query.get(id)
    if film:
        result = film_schema.dump(film)
        return jsonify(result), 200
    else:
        return {'message': 'Film not found'}, 404

@app.route('/films', methods=['POST'])
@jwt_required()
def post_film():
    data = request.get_json()
    if not data:
      return {'message': "Invalid data"}, 400
    film = film_schema.load(data)
    db.session.add(film)
    db.session.commit()
    return film_schema.dump(film), 201

@app.route('/films/<int:id>', methods=['PUT'])
@jwt_required()
def put_film(id):
    film = Film.query.get(id)
    if not film:
        return {'message': 'Film not found'}, 404
    data = request.get_json()
    if not data:
      return {'message': "Invalid data"}, 400
    updated_film = film_schema.load(data, instance=film)
    db.session.commit()
    return film_schema.dump(updated_film), 200

@app.route('/films/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_film(id):
    film = Film.query.get(id)
    if film:
        db.session.delete(film)
        db.session.commit()
        return {'message': 'Film deleted'}, 200
    else:
        return {'message': 'Film not found'}, 404

if __name__ == '__main__':
  app.run(debug=True)