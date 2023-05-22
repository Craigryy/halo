from flask import Flask , jsonify  ,request ,make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Favour98@localhost/milo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)


class User(db.Model):

    """User model for authentication."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer(),unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True)
    LoggedIn = db.Column(db.Boolean, default=True)
    Book = db.relationship('BookModel', backref='owner', lazy='dynamic')

    def json(self):
        '''Display output as json object.'''

        return {id: self.id, 'username': self.username,
                'password': self.password, 'LoggedIn': self.LoggedIn}


    def __repr__(self):
        return "<User(username='%s', email='%s')>" % (self.username,
                                                      self.email)
class BookCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_by = db.Column(db.String(64))
    books = db.relationship('BookModel', backref='bookModel', cascade="all, delete-orphan", lazy='dynamic')

    def json(self):
        ''' Display output as JSON object.'''

        return {
            "id": self.id,
            "name": self.name,
            "items_count": len(self.items.all()),
            "created_at": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": self.created_by,
        }


class BookModel(db.Model):

    """BookModel defined."""

    __tablename__ = 'BookModels'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('book_category.id'), nullable=False)
    category = db.relationship('BookCategory', backref=db.backref('books', lazy=True))

    def json(self):
        ''' Display output as JSON object.'''

        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
            "done": self.done,
        }

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# create a user
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['loggedIn'] = user.loggedIn
        output.append(user_data)

    return jsonify({'users' : output})

# get all users
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify([user.json() for user in users]), 200)
  except e:
    return make_response(jsonify({'message': 'error getting users'}), 500)

# get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting user'}), 500)

# update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.username = data['username']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error updating user'}), 500)

# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting user'}), 500)


@app.route('/categories/', methods=['POST'])
@token_required
def add_book_category(id):
    '''Create a category for a book.'''

    book_category = BookCategory.query.filter_by(id=id).first()

    if not book_category:
        return jsonify('category with  was not found')

    data = request.get_json()
    BookModel = BookModel(title=data['title'])
    BookModel.category_id = book_category.id
    BookModel.save()

    return jsonify({'message': 'Book category successfully saved.'})


@app.route('/categories/', methods=['GET'])
@token_required
def list_book_category():
    '''list all category for a book.'''

    return BookCategory.query.all()


@app.route("/PUT/categories/<int:id>", methods=['PUT'])
def update(id):
    '''Update a book category. '''

    book_category = BookCategory.query.filter_by(id=id).first()
    if not book_category:
        return jsonify({'message': 'category with id was not found in database'})

    BookModel = BookModel.query.get(id)
    if not BookModel:
        return jsonify({'message': 'BookModel was not found'})

    if request.method == 'PUT':

        if BookModel.id == BookCategory.id:
            data = request.get_json()
            book_category.name = data['name']
            BookModel.id = BookCategory.id
            BookModel.save()

            return jsonify({'message': 'book category successfully updated'})


@app.route("/categories/<int:id>", methods=['DELETE'])
def delete(id):
    '''Delete a book category. '''

    if request.method == 'DELETE':
        book = BookModel.query.filter_by(id=id).first()
        if book:
            BookModel.delete()
            return jsonify({'message': 'BookModel successfully deleted'})

if __name__=='__main__':
   app.run(debug=True)