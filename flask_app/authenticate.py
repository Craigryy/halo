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
    return make_response(jsonify({"message": error_message}), 500)


@auth_app.route("/users/<int:id>", methods=["DELETE"])
@token_required
def delete_user(current_user, id):
    """Delete a single user from the database."""
    if not current_user:
        return jsonify({"message": "Cannot perform that function!"})
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            user.delete()
            return make_response(jsonify({"message": "user deleted"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except Exception as e:
        error_message = f"Error deleting user: {str(e)}"
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
