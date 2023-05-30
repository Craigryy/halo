from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Favour98@localhost/kittie'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'jesusislord'
port = 5000

db = SQLAlchemy(app)


class Base(db.Model):

    ''' Abstract Base class used to define id.'''

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    # saves the data
    def save(self):
        db.session.add(self)
        db.session.commit()

    # deletes the data
    def delete(self):
        db.session.add(self)
        db.session.delete(self)
        db.session.commit()


class User(Base):

    """User model for authentication."""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    Book = db.relationship('BookModel', backref='user', lazy='dynamic')

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'public_id': self.public_id, 'password': self.password, 'admin': self.admin}


class BookCategory(Base):
    """BookCategory table defined """

    __tablename__ = 'BookCategorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    books = db.relationship('BookModel', backref='category',
                            cascade="all, delete-orphan", lazy='dynamic')

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'created_by': self.created_by}


class BookModel(Base):

    """BookModel defined."""

    __tablename__ = 'BookModels'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('BookCategorys.id'))

    def to_json(self):
        return {'id': self.id, 'title': self.title, 'author': self.author}


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
            return jsonify({'message': 'Token is invalid!'}.format(e)), 401

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
        return make_response(jsonify({'message': 'error updating user'}.format(e)), 500)


# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user,id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            user.delete()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting user'}), 500)


# create a loggin route
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})



# Create a new book in the category
@app.route("/categories/", methods=['POST'])
@token_required
def addnew_bookcategory(current_user):
    ''' create a book in the category. '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    json_data = request.get_json()
    name, created_by = json_data['name'], json_data['created_by']
    category = BookCategory(name=name, created_by=created_by,user_id=current_user.id)
    category.save()

    return jsonify({'BookCategory': 'category created'})

#


@app.route('/categories/', methods=['GET'])
@token_required
def list_book_category(current_user):
    '''list all category for a book.'''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    categories = BookCategory.query.all()

    return make_response(jsonify([category.to_json() for category in categories]), 200)


@app.route('/categories/<int:id>', methods=['GET'])
@token_required
def get_book_category(current_user,id):
    '''Get a single book category.'''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    try:
        category = BookCategory.query.filter_by(id=id,user_id=current_user.id).first()
        if category:
            return make_response(jsonify({'category': category.to_json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting user'}.format(e)), 500)


@app.route("/categories/<int:id>", methods=['PUT'])
@token_required
def update(current_user,id):
    '''Update a book category. '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    try:
        category = BookCategory.query.filter_by(id=id,user_id=current_user.id).first()
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
def delete(current_user,id):
    '''Delete a book category. '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    try:
        book = BookCategory.query.filter_by(id=id,user_id=current_user.id).first()
        if book:
            book.delete()
            return jsonify({'message': 'BookModel successfully deleted'})
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e :
        return make_response(jsonify({'message': 'error deleting user'}.format(e)), 500)


# Create book
@app.route('/categories/<int:id>/books/', methods=['POST'])
@token_required
def create_book(current_user,id):
    '''Create a book. '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    category = BookCategory.query.filter_by(id=id,user_id=current_user.id).first()
    if not category:
        return make_response(jsonify(('category with id:{} was not found' .format(id))))
    json_data = request.get_json()
    title, author = json_data['title'], json_data['author']
    book = BookModel(title=title, author=author)
    book.category_id = category.id
    book.save()

    return jsonify({'book': "good"})


# Update book
@app.route('/categories/<int:id>/books/<int:book_id>', methods=['PUT'])
@token_required
def update_book(current_user,id, book_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    category = BookCategory.query.filter_by(id=id).first()

    if not category:
        return make_response(('bucket list with id:{} was not found' .format(id)))

    book = BookModel.query.get(id)
    if not book:
        return make_response(('book with id:{} was not found' .format(book_id)))

    book = BookModel.query.get(id)
    if book:
        book.title = request.json.get('title', book.title)
        book.author = request.json.get('author', book.author)
        book.category_id = request.json.get('category_id', book.category_id)
        book.category_id = category.id
        book.save()
        return make_response( jsonify({"message": "Book updated successfully", "book": book.to_json()}), 200)

    return make_response(jsonify({"message": "Book not found"}), 404)

# Delete book


@app.route('/categories/<int:id>/books/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user,id, book_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    bookcategory = BookCategory.query.filter_by(id=id,user_id=current_user.id).first()

    if not bookcategory:
        return make_response(('book category with id:{} was not found' .format(book_id)))

    book = BookModel.query.get(id)
    if book :
        book.delete()
        return make_response(jsonify({"message": "Book deleted successfully"}), 200)

    return make_response(jsonify({"message": "Book not found"}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
