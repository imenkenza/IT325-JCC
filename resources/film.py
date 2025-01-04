import uuid
from flask import Blueprint,  abort
from flask.views import MethodView
from flask_smorest import Blueprint
from models.film import FilmModel
from schemas import FilmSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db

blp = Blueprint("Films", "films", description="Operations on films")

@blp.route("/films")
class FilmList(MethodView):
    @blp.response(200, FilmSchema(many=True))
    def get(self):
        """Get all films"""
        return FilmModel.query.all()

    @blp.arguments(FilmSchema)
    @blp.response(201, FilmSchema)
    def post(self, film_data):
        """Create a new film"""
        film_data['id'] = uuid.uuid4()
        film = FilmModel(**film_data)
        try:
            db.session.add(film)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A film with that title already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the film.")
        return film

@blp.route("/film/<int:film_id>")
class Film(MethodView):
    @blp.response(200, FilmSchema)
    def get(self, film_id):
        """Get a film by ID"""
        film = FilmModel.query.get_or_404(film_id)
        return film

    @blp.arguments(FilmSchema)
    @blp.response(200, FilmSchema)
    def put(self, film_data, film_id):
        """Update a film by ID"""
        film = FilmModel.query.get_or_404(film_id)
        
        # Update the film with the new data
        for key, value in film_data.items():
            setattr(film, key, value)
        
        db.session.commit()
        return film

    @blp.response(204)
    def delete(self, film_id):
        """Delete a film by ID"""
        film = FilmModel.query.get_or_404(film_id)
        db.session.delete(film)
        db.session.commit()
        return {"message": "Film deleted"}, 204