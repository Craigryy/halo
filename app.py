from flask import Flask , jsonify  ,request ,make_response, url_for,g
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Favour98@localhost/milk'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SECRET_KEY']='jesusislord'

db = SQLAlchemy(app)


class User(db.Model):

    """User model for authentication."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    Book= db.relationship('BookModel', backref='user', lazy='dynamic')



class BookCategory(db.Model):
    """BookCtegory table defined """

    __tablename__='BookCategorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.String(100))
    books = db.relationship('BookModel', backref='category',primaryjoin='BookCategory.id == BookModel.category_id',cascade="all, delete-orphan", lazy='dynamic')


    def __init__(self, name,created_by):
        self.name = name
        self.created_by = created_by



    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [book.serialize() for book in self.books]
        }

    



class BookModel(db.Model):

    """BookModel defined."""

    __tablename__ = 'BookModels'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('BookCategorys.id'))


    def __init__(self, title):
        self.title = title


    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done,
            'user_id': self.user_id,
            'category_id': self.category_id
            }
    

    
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


def bad_request(message):
    '''Request that are bad '''

    # response to invalid/bad  request.
    response = jsonify({'message': message, 'status': '400'})
    response.status_code = 400
    return response


def Unauthorized(message=None):
    ''' Restricted in perfroming these action .'''

    # if a message/response if secret key is given.
    if message is None:
        if app.config['SECRET_KEY']:
            message = 'Authentication with your token is needed.'
        else:
            message = 'Token is required.'
    response = jsonify({'message': message, 'status': 401})
    response.status_code = 401
    if app.config['SECRET_KEY']:
        response.headers['Location'] = url_for('new_user')
    return response


def Method_not_allowed():
    '''Method not allowed'''

    # message to response to method not allowed
    response = jsonify({'status': 405, 'error': 'method not allowed'})
    response.status_code = 405
    return response


#create a token
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
def get_all_users():

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'New user created!"'})


@app.route('/user/<public_id>', methods=['GET'])
# @token_required
def get_one_user( public_id):

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

# update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.rname = data['name']
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

#create a loggin
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


@app.route("/categories/<int:id>/books/",methods=['POST'])
#Create a new book in the category
def addnew_book(id):

    ''' create a book in the category. '''

    bookcategory = BookCategory.query.\
                filter_by(created_by=g.user.username).\
                filter_by(id=id).first()

    if not BookCategory:
        return bad_request('bucket list with id:{} was not found' .format(id))

    json_data = request.get_json()
    title, done = json_data['title'], json_data['done']            
    bookmodel = BookModel(title=title, done=True, date_modified=datetime.utcnow())
    bookmodel.category_id=bookcategory.id
    db.session.add(bookmodel)
    db.session.commit()

    return jsonify({'Book_Model':BookModel.to_json()})



@app.route('/categories/', methods=['POST'])
def add_book_category():
    '''Create a category for a book.'''

    data = request.get_json()
    Book_category = BookCategory(name=data['name'],created_by=data['created_by'])
    db.session.add(Book_category)
    db.session.commit()

    return jsonify({'message': 'Book category successfully saved.'})



@app.route('/categories/', methods=['GET'])
def list_book_category():
    '''list all category for a book.'''

    categories = BookCategory.query.all()

    output = []

    for books in categories:
        user_data = {}
        user_data['public_id'] = books.name
        user_data['created_by'] = books.created_by
        output.append(user_data)

    return jsonify({'users' : output})



@app.route("/categories/<int:id>", methods=['PUT'])
def update(id):
    '''Update a book category. '''

    book_category = BookCategory.query.filter_by(id=id).first()
    if not book_category:
        return jsonify({'message': 'category with id was not found in database'})


    if book_category:
        book_category.name = request.json.get('name', book_category.name)
        book_category.created_by = request.json.get('created_by', book_category.created_by)
        db.session.commit()

        return jsonify({"message": "Book category successfully updated", "book": book_category.serialize()}), 200



@app.route("/categories/<int:id>", methods=['DELETE'])
def delete(id):
    '''Delete a book category. '''

    book = BookCategory.query.filter_by(id=id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'BookModel successfully deleted'})



if __name__=='__main__':
   app.run(debug=True)