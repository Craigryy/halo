from flask import Flask , jsonify  ,request ,make_response
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



    # def json(self):
    #     '''Display output as json object.'''

    #     return {id: self.id, 'name': self.name,
    #             'password': self.password, 'admin': self.admin}


    # def __repr__(self):
    #     return "<User(name='%s', email='%s')>" % (self.name,
    #                                                   self.email)
class BookCategory(db.Model):
    """BookCtegory table defined """

    __tablename__='BookCategorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.String(100))
    books = db.relationship('BookModel', backref='category',primaryjoin='BookCategory.id == BookModel.category_id',cascade="all, delete-orphan", lazy='dynamic')
    

    # def json(self):
    #     ''' Display output as JSON object.'''

    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "items_count": len(self.items.all()),
    #         "created_at": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
    #         "updated_at": self.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
    #         "created_by": self.created_by,
    #     }


class BookModel(db.Model):

    """BookModel defined."""

    __tablename__ = 'BookModels'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('BookCategorys.id'))


    


    # def json(self):
    #     ''' Display output as JSON object.'''

    #     return {
    #         "id": self.id,
    #         "title": self.title,
    #         "created_at": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
    #         "updated_at": self.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
    #         "done": self.done,
    #     }

#create a test routespip
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


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
    return jsonify({'message' : 'New user created!'})
    # except Exception as e :
    #    return jsonify({'message':'otilo'})

# get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404
except e:
    return make_response(jsonify({'message': 'error getting user'}), 500)

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

    if not auth or not auth.name or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.name).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

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