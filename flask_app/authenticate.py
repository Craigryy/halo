<<<<<<< HEAD
import jwt
import time
import uuid
import json
from functools import wraps
from flask_jwt_extended import create_access_token
from flask_bcrypt import check_password_hash, generate_password_hash
from datetime import timedelta, timezone, datetime
from flask import Blueprint, jsonify, make_response, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, unset_jwt_cookies , get_jwt
from .model import User, db
from config import app

jwt = JWTManager(app)
auth_app = Blueprint("auth_app", __name__)

# @auth_app.route('/test', methods=["GET"])
# def test():
#     """
#     A test route.
#     """
#     return make_response(jsonify({"message": "test route"}), 200)
@auth_app.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    """
    Get all users from the database.
    """
    try:
        # Get the user ID of the currently authenticated user
        current_user_id = get_jwt_identity()
        
        # Query the currently logged-in user based on their public_id
        current_user = User.query.filter_by(public_id=current_user_id).first()

        if current_user:
            # Retrieve all users from the database (remove the unnecessary filter)
            users = User.query.all()
            
            return make_response(jsonify([user.to_json() for user in users]), 200)
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        error_message = f"Error listing users: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)


@auth_app.route('/auth/register', methods=["POST"])
def register_user():
    """
    Register a new user.
    """
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="sha256")
    new_user = User(public_id=str(uuid.uuid4()), name=data["name"], password=hashed_password, admin=False)
    new_user.save()
    return jsonify({"message": "New user registered!"})

@auth_app.route('/user/<int:public_id>', methods=['GET'])
@jwt_required()
def get_one_user(public_id):
    """
    Get a single user from the database.
    """
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "No user found!"})
    user_data = {
        "public_id": user.public_id,
        "name": user.name,
        "password": user.password,
        "admin": user.admin,
    }
    return jsonify({"user": user_data})

@auth_app.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """
    Update a single user in the database.
    """
=======
import datetime
import jwt
import time
import uuid
from functools import wraps

from flask import Blueprint, Flask, jsonify, make_response, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from .model import User, db

auth_app = Blueprint("auth_app", __name__)


def token_required(f):
    """
    A decorator to require a valid token in the "x-access-token" header.

    Args:
        f (function): The function to decorate.

    Returns:
        function: The decorated function with token authentication.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except Exception as e:
            error_message = f"Token is invalid!: {str(e)}"
            return make_response(jsonify({"message": error_message}), 500)

        return f(current_user, *args, **kwargs)

    return decorated


@auth_app.route("/test", methods=["GET"])
def test():
    """A test route."""
    return make_response(jsonify({"message": "test route"}), 200)


@auth_app.route("/user", methods=["GET"])
@token_required
def get_all_users(current_user):
    """Get all users from the database."""
    if not current_user:
        return jsonify({"message": "Cannot perform that function!"})

    users = User.query.all()

    return make_response(jsonify([user.to_json() for user in users]), 200)


@auth_app.route("/auth/login", methods=["POST"])
def create_user():
    """Create a new user endpoint."""
    data = request.get_json()

    hashed_password = generate_password_hash(data["password"], method="sha256")

    new_user = User(
        public_id=str(uuid.uuid4()), name=data["name"], password=hashed_password, admin=False
    )
    new_user.save()
    return jsonify({"message": "New user created!"})


@auth_app.route("/user/<int:public_id>", methods=["GET"])
@token_required
def get_one_user(current_user, public_id):
    """Get a single user from the database."""
    if not current_user:
        return jsonify({"message": "Cannot perform that function!"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "No user found!"})

    user_data = {}
    user_data["public_id"] = user.public_id
    user_data["name"] = user.name
    user_data["password"] = user.password
    user_data["admin"] = user.admin

    return jsonify({"user": user_data})


@auth_app.route("/users/<int:id>", methods=["PUT"])
@token_required
def update_user(current_user, id):
    """Update a single user in the database."""
    if not current_user:
        return jsonify({"message": "Cannot perform that function!"})
>>>>>>> origin/master
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.name = data["name"]
            user.password = data["password"]
            user.admin = data["admin"]
            db.session.commit()
            return make_response(jsonify({"message": "user updated"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except Exception as e:
        error_message = f"Error updating user: {str(e)}"
<<<<<<< HEAD
        return make_response(jsonify({"message": error_message}), 500)

@auth_app.route('/user/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    """
    Delete a single user from the database.
    """
=======
    return make_response(jsonify({"message": error_message}), 500)


@auth_app.route("/users/<int:id>", methods=["DELETE"])
@token_required
def delete_user(current_user, id):
    """Delete a single user from the database."""
    if not current_user:
        return jsonify({"message": "Cannot perform that function!"})
>>>>>>> origin/master
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            user.delete()
            return make_response(jsonify({"message": "user deleted"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except Exception as e:
        error_message = f"Error deleting user: {str(e)}"
<<<<<<< HEAD
        return make_response(jsonify({"message": error_message}), 500)

@auth_app.route('/login', methods=["POST"])
def create_token():
    """
    Create a token upon login.
    """
    name = request.json.get("name", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(name=name).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    access_token = create_access_token(identity=user.public_id)
    return jsonify({
        "name": name,
        "access_token": access_token
    })

@auth_app.after_request
def refresh_expiring_jwts(response):
    """
    Refresh token after expiring.
    """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response

@auth_app.route("/logout", methods=["POST"])
def logout():
    """
    Route for logout.
    """
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response 
=======
    return make_response(jsonify({"message": error_message}), 500)


@auth_app.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return a token."""
    secret_key = current_app.config["SECRET_KEY"]
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {"public_id": user.public_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            secret_key,
        )

        return jsonify({"token": token})

    return make_response(
        "Could not verify",
        401,
        {"WWW-Authenticate": 'Basic realm="Login required!"'},
    )
>>>>>>> origin/master
