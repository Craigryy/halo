'''Models defined for APi  '''

from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Favour98@localhost/halo'
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
    category = db.relationship('BookCategory', backref='owner', lazy='dynamic')

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'public_id': self.public_id, 'password': self.password, 'admin': self.admin}


class BookCategory(Base):
    """BookCategory table defined """

    __tablename__ = 'BookCategorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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
    category_id = db.Column(db.Integer, db.ForeignKey('BookCategorys.id'))

    def to_json(self):
        return {'id': self.id, 'title': self.title, 'author': self.author}
