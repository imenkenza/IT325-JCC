from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import FilmSchema
from models.film import FilmModel
from db import db

blp = Blueprint("Films", __name__, description="Operations on films")


@blp.route("/film")
class FilmList(MethodView):
    @blp.response(200, FilmSchema(many=True))
    def get(self):
        return list(db.get("films", {}).values())

    @blp.arguments(FilmSchema)
    @blp.response(201, FilmSchema)
    def post(self, new_film):
        try:
            film_id = max(film.id for film in db.get("films", {}).values()) + 1
        except ValueError:
            film_id = 1

        film = FilmModel(id=film_id, **new_film)
        if "films" not in db:
            db["films"] = {}
        db["films"][film_id] = film
        return film


@blp.route("/film/<int:film_id>")
class FilmById(MethodView):
    @blp.response(200, FilmSchema)
    def get(self, film_id):
        try:
            return db["films"][film_id]
        except KeyError:
            abort(404, message="Film not found")

    @blp.arguments(FilmSchema)
    @blp.response(200, FilmSchema)
    def put(self, updated_film, film_id):
        try:
            film= db["films"][film_id]
            for key, value in updated_film.items():
                setattr(film,key,value)
            return film
        except KeyError:
           abort(404, message="Film not found")


    def delete(self, film_id):
        try:
            del db["films"][film_id]
            return {"message": "Film deleted."}
        except KeyError:
            abort(404, message="Film not found")

@blp.route("/film/genre/<string:genre>")
class FilmByGenre(MethodView):
    @blp.response(200, FilmSchema(many=True))
    def get(self, genre):
        films=db.get("films", {}).values()
        filtered_films=[film for film in films if film.genre == genre]
        return filtered_films
@blp.route("/film/category/<string:category>")
class FilmByCategory(MethodView):
     @blp.response(200, FilmSchema(many=True))
     def get(self, category):
         films=db.get("films", {}).values()
         filtered_films=[film for film in films if film.category == category]
         return filtered_films