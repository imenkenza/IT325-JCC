from flask import Flask
from flask_smorest import Api

from db import db
import models  


from resources.film import blp as Film_Blueprint
from resources.venue import blp as Venue_Blueprint
from resources.event import blp as Event_Blueprint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "JCC Scheduling REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()


    api.register_blueprint(Film_Blueprint)
    api.register_blueprint(Venue_Blueprint)
    api.register_blueprint(Event_Blueprint)

    return app