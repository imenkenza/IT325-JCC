""" import uuid
from flask import abort, request
from flask_smorest import Blueprint
from flask.views import MethodView
from db import specializations

from schemas import SpecializationSchema

blp = Blueprint("specialization", __name__, description="Operations on specialization")

@blp.route("/specialization/<string:specialization_id>")
class Specialization(MethodView):
    def get(self, specialization_id):
        try:
        # Here you might also want to add the course_items in this specialization
        # We'll do that later on in the course
            return specializations[specialization_id]
        except KeyError:
            abort(404, message="Specialization not found.")
    def delete(self, specialization_id):
        try:
            del specializations[specialization_id]
            return {"message": "Specialization deleted."}
        except KeyError:
            abort(404, message="Specialization not found.")
@blp.route("/specialization")
class SpecializationList(MethodView):
    def get(self):
        return {"specializations": list(specializations.values())}
    def post(self):
        specialization_data = request.get_json()
        if "name" not in specialization_data:
            abort(
                400,
                message="Bad request. Ensure 'name' is included in the JSON payload.",
            )
        for specialization in specializations.values():
            if specialization_data["name"] == specialization["name"]:
                abort(400, message=f"Specialization already exists.")
        specialization_id = uuid.uuid4().hex
        specialization = {**specialization_data, "id": specialization_id}
        specializations[specialization_id] = specialization
        return specialization """
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import SpecializationModel
from schemas import SpecializationSchema


blp = Blueprint("Specializations", "specializations", description="Operations on specializations")


@blp.route("/specialization/<string:specialization_id>")
class Specialization(MethodView):
    @blp.response(200, SpecializationSchema)
    def get(self, specialization_id):
        specialization = SpecializationModel.query.get_or_404(specialization_id)
        return specialization

    def delete(self, specialization_id):
        specialization = SpecializationModel.query.get_or_404(specialization_id)
        db.session.delete(specialization)
        db.session.commit()
        return {"message": "Specialization deleted"}, 200


@blp.route("/specialization")
class SpecializationList(MethodView):
    @blp.response(200, SpecializationSchema(many=True))
    def get(self):
        return SpecializationModel.query.all()

    @blp.arguments(SpecializationSchema)
    @blp.response(201, SpecializationSchema)
    def post(self, specialization_data):
        specialization = SpecializationModel(**specialization_data)
        try:
            db.session.add(specialization)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A specialization with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the specialization.")

        return specialization