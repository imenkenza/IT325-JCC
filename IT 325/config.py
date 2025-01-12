import os
from dotenv import load_dotenv

load_dotenv()

class Config:
     SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
     SECRET_KEY = os.environ.get("SECRET_KEY")
     JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
     MAIL_SERVER = os.environ.get("MAIL_SERVER")
     MAIL_PORT = os.environ.get("MAIL_PORT")
     MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") == 'True'
     MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
     MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")