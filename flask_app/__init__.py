from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_app.authenticate import auth_app
from flask_app.bookmodel import book_app
from flask_app.category import category_app
from config import POSTGRES_HOST,POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

db = SQLAlchemy()


def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Register blueprints

    app.register_blueprint(auth_app)
    app.register_blueprint(book_app)
    app.register_blueprint(category_app)

    return app
