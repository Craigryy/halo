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