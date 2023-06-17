import os

# Check if running inside Docker container
if os.environ.get('DOCKER_ENV'):
    POSTGRES_HOST = 'database'
else:
    POSTGRES_HOST = 'localhost'

#Set environment
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')  # Update 'localhost' to 'database'
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'halo')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'Favour98')
POSTGRES_SECRET_KEY = os.environ.get('POSTGRES_SECRET_KEY', 'jesusislord')
FLASK_PORT = os.environ.get('FLASK_PORT', '5000')

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] =f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = POSTGRES_SECRET_KEY
port = FLASK_PORT

# Initialize the database
db = SQLAlchemy()
db.init_app(app)


