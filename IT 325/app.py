"""from flask import Flask
from flask_migrate import Migrate
from db import create_app, db
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import os
import yaml

app = create_app()
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.config['SWAGGER'] = {
     'title': 'Movie API',
     'uiversion': 3,
      "specs_route" : "/apidocs",
     "specs": [
         {
           "endpoint": 'apispec_1',
           "route": '/apispec_1.json',
           "rule_filter": lambda rule: True,
          "model_filter": lambda tag: True
         }
       ]
 }

with open("swagger.yaml", "r") as f:
     swagger_config = yaml.safe_load(f)

Swagger(app, template=swagger_config)


from resources import user as user_resource
from resources import film as film_resource
from resources import venue as venue_resource
from resources import event as event_resource
from resources import schedule as schedule_resource

if __name__ == '__main__':
     with app.app_context():
         db.create_all()
     app.run(debug=True)"""
from flask import Flask
from flask_migrate import Migrate
from db import create_app, db
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import os
import yaml

app = create_app()
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.config['SWAGGER'] = {
         'title': 'Movie API',
         'uiversion': 3,
         "specs_route" : "/apidocs",
         "specs": [
             {
                  "endpoint": 'apispec_1',
                  "route": '/apispec_1.json',
                  "rule_filter": lambda rule: True,
                  "model_filter": lambda tag: True
              }
          ]
      }

with open("swagger.yaml", "r") as f:
         swagger_config = yaml.safe_load(f)

Swagger(app, template=swagger_config)

from resources.user import app as user_app
from resources.film import app as film_app
from resources.venue import app as venue_app
from resources.event import app as event_app
from resources.schedule import app as schedule_app

if __name__ == '__main__':
         with app.app_context():
             db.create_all()
         app.run(debug=True)