from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask

db = SQLAlchemy()

def create_app():
     app = Flask(__name__)
     app.config.from_object(Config)
     db.init_app(app)

     return app