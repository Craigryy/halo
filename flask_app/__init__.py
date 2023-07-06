import time
from flask import Flask
from flask_app.authenticate import auth_app
from flask_app.bookmodel import book_app
from flask_app.category import category_app
from flask_swagger_ui import get_swaggerui_blueprint
from config import POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, db, POSTGRES_SECRET_KEY
import yaml

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = POSTGRES_SECRET_KEY
    app.static_folder = 'static'


    # Introduce a delay before initializing the database
    time.sleep(10)  # Adjust the delay as needed

    # Initialize the database
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # Register blueprints
    app.register_blueprint(auth_app)
    app.register_blueprint(book_app)
    app.register_blueprint(category_app)

    # Load the OpenAPI specification from the YAML file
    with open('static/openapi.yaml', 'r') as file:
        openapi_spec = yaml.safe_load(file)

    # Create the Swagger UI blueprint
    SWAGGER_URL = '/api/docs'  # URL for accessing the Swagger UI
    API_URL = '/static/openapi.yaml'  # URL for the OpenAPI specification file
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Halo API",  # Displayed name in the Swagger UI
            'spec': openapi_spec  # Pass the loaded OpenAPI spec to Swagger UI
        }
    )

    # Register the Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app


