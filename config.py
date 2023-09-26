import os
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_bcrypt import bcrypt,Bcrypt
from flask import Flask, jsonify, request, make_response
from flask_swagger_ui import get_swaggerui_blueprint


# Check if running inside Docker container
if os.environ.get('DOCKER_ENV'):
    POSTGRES_HOST = 'database'
else:
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')

POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', 5432))
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'halo')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'Favour98')
POSTGRES_SECRET_KEY = os.environ.get('POSTGRES_SECRET_KEY', 'jesusislord')
FLASK_PORT = int(os.environ.get('FLASK_PORT', 5000))

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory

# Create the Flask application
app = Flask(__name__, static_folder='reactFrontenddd/build', static_url_path='')

if 'REACT_API_URL' is os.environ:
    cors = CORS(app, resources={r"*": {"origins": 'REACT_API_URL' }})
   

    # Configure the database URI conditionally based on Heroku or local
if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = POSTGRES_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

port = FLASK_PORT

# Initialize the database
db = SQLAlchemy()
db.init_app(app)
