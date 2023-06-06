from flask import jsonify, request, make_response,Blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from .model import User,db



auth_app = Blueprint('auth_app', __name__)


# create a test route


@auth_app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# create a token_required decorator which requires a header "x-access-token" and a token .
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, auth_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except Exception as e:
            error_message = f"Token is invalid!: {str(e)}"
            return make_response(jsonify({'message': error_message}), 500)

        return f(current_user, *args, **kwargs)

    return decorated

# create a user

# create an endpoint to get all users


@auth_app.route('/user', methods=['GET'])
@token_required
def get_all_users():
    '''Get all users '''

    users = User.query.all()

    return make_response(jsonify([user.to_json() for user in users]), 200)


# create a new user endpoint
@auth_app.route('/auth/login', methods=['POST'])
# @token_required
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    name=data['name'], password=hashed_password, admin=False)
    new_user.save()
    return jsonify({'message': 'New user created!"'})


# Write a function named `get_one_user` which takes in a public id using `GET` method,
# and assign to the static route of ('/user/<int:public_id>')
@auth_app.route('/user/<int:public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    '''End point to access a single user in the database.'''

    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


# update a user

# Write a function named `update_user` which takes in an id using `PUT` method,
# and assign to the static route of ('/users/<int:id>')
@auth_app.route('/users/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    '''End point to update a single user in the database.'''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.name = data['name']
            user.password = data['password']
            user.admin = data['admin']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        error_message = f"Error updating user: {str(e)}"
    return make_response(jsonify({'message': error_message}), 500)


# Write a function named `delete_user` which takes in an id using `DELETE` method,
# and assign to the static route of ('/users/<int:id>')
@auth_app.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    '''End point to delete a single user in the database.'''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            user.delete()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        error_message = f"Error deleting user: {str(e)}"
    return make_response(jsonify({'message': error_message}), 500)


# create a loggin route ,which requires a username and a password for basic,
# authentication.
@auth_app.route('/login', methods=['POST'])
def login():
    '''create a login route'''
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, auth_app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
