import yaml
import os
from flask import Flask, jsonify, request, make_response
from flask.helpers import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import time
import yaml
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from config import (
    POSTGRES_HOST,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    db,
    POSTGRES_SECRET_KEY,
)
from flask_app.authenticate import auth_app
from flask_app.bookmodel import book_app
from flask_app.category import category_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    """
    Create the Flask application, configure the database, and register blueprints.

    Returns:git
        Flask: The Flask application instance.
    """
    # Create the Flask application
    app = Flask(__name__, static_folder='../reactFrontenddd/build', static_url_path='')
    jwt = JWTManager(app)

    # Configure CORS for all origins in production, or specific origins in development
    if os.environ.get('FLASK_ENV') == 'production':
        # In production, allow requests from the frontend URL
        frontend_url = os.environ.get('FRONTEND_URL', '*')
        cors = CORS(app, resources={r"/*": {"origins": frontend_url}})
    else:
        # In development, allow all origins
        cors = CORS(app)

    # Configure database
    if 'DATABASE_URL' in os.environ:
        # For Render PostgreSQL - convert from postgres:// to postgresql://
        database_url = os.environ['DATABASE_URL']
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    elif 'DATABASE_URL_HEROKU' in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL_HEROKU']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = POSTGRES_SECRET_KEY
    app.static_folder ='../reactFrontenddd/build'


    # Initialize the database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(auth_app)
    app.register_blueprint(book_app)
    app.register_blueprint(category_app)

    # Load the OpenAPI specification from the YAML file
    with open("static/openapi.yaml", "r") as file:
        openapi_spec = yaml.safe_load(file)

    # Create the Swagger UI blueprint
    SWAGGER_URL = "/api/docs"  # URL for accessing the Swagger UI
    API_URL = "/static/openapi.yaml"  # URL for the OpenAPI specification file
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "Halo API",  # Displayed name in the Swagger UI
            "spec": openapi_spec,  # Pass the loaded OpenAPI spec to Swagger UI
        },
    )

    # Register the Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.before_request
    def before_request():
        if request.method == "OPTIONS" or request.method == "options":
            # Handle preflight request (OPTIONS)
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            }
            response = make_response()
            for key, value in headers.items():
                response.headers[key] = value
            return response


    @app.route("/")
    def serve():
        return app.send_static_file('index.html')

    @app.errorhandler(404)
    def not_found(err):
        return send_from_directory('../reactFrontenddd/build','index.html')



    return app
