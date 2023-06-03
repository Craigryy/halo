from flask import jsonify, request, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from model import BookCategory, User, app, db

# create a test route


@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# create a token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except Exception as e:
            error_message = f"Token is invalid!: {str(e)}"
            return make_response(jsonify({'message': error_message}), 500)

        return f(current_user, *args, **kwargs)

    return decorated

# create a user

# create an endpoint to get all users


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    users = User.query.all()

    return make_response(jsonify([user.to_json() for user in users]), 200)


# create a new user endpoint
@app.route('/auth/login', methods=['POST'])
# @token_required
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    name=data['name'], password=hashed_password, admin=False)
    new_user.save()
    return jsonify({'message': 'New user created!"'})


# endpoint to get a single user
@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
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
@app.route('/users/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    if not current_user.admin:
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


# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    if not current_user.admin:
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


# create a loggin route
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


# Create a new book in the category
@app.route("/categories/", methods=['POST'])
@token_required
def addnew_bookcategory(current_user):
    ''' create a book in the category. '''
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    json_data = request.get_json()
    name, created_by = json_data['name'], json_data['created_by']
    category = BookCategory(
        name=name, created_by=created_by, user_id=current_user.id)
    category.save()

    return jsonify({'BookCategory': category.to_json})

#


@app.route('/categories/', methods=['GET'])
@token_required
def list_book_category(current_user):
    '''list all category for a book.'''
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    categories = BookCategory.query.all()

    return make_response(jsonify([category.to_json() for category in categories]), 200)


@app.route('/categories/<int:id>', methods=['GET'])
@token_required
def get_book_category(current_user, id):
    '''Get a single book category.'''
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        category = BookCategory.query.filter_by(
            id=id, user_id=current_user.id).first()
        if category:
            return make_response(jsonify({'category': category.to_json()}), 200)
        return make_response(jsonify({'message': 'category not found'}), 404)
    except Exception as e:
        error_message = f"Error getting category: {str(e)}"
    return make_response(jsonify({'message': error_message}), 500)


@app.route("/categories/<int:id>", methods=['PUT'])
@token_required
def update(current_user, id):
    '''Update a book category. '''
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        category = BookCategory.query.filter_by(
            id=id, user_id=current_user.id).first()
        if category:
            data = request.get_json()
            category.name = data['name']
            category.created_by = data['created_by']
            db.session.commit()
            return make_response(jsonify({'message': 'category updated'}), 200)
        return make_response(jsonify({'message': 'category not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating category'}.format(e)), 500)


@app.route("/categories/<int:id>", methods=['DELETE'])
@token_required
def delete(current_user, id):
    '''Delete a book category. '''
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        book = BookCategory.query.filter_by(
            id=id, user_id=current_user.id).first()
        if book:
            book.delete()
            return jsonify({'message': 'category successfully deleted'})
        return make_response(jsonify({'message': 'category not found'}), 404)
    except Exception as e:
        error_message = f"Error deleting category: {str(e)}"
    return make_response(jsonify({'message': error_message}), 500)
