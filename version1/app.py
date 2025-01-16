import os
from flask import Flask
from flask_smorest import Api
from resources.film import blp as FilmBlueprint
from resources.venue import blp as VenueBlueprint
from resources.events import blp as EventBlueprint


def create_app():
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "JCC Cinephile Schedule REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/"
    #db.init_app(app) #remove this line
    api = Api(app)
    api.register_blueprint(FilmBlueprint)
    api.register_blueprint(VenueBlueprint)
    api.register_blueprint(EventBlueprint)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)