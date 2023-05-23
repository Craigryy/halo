# from flask import Flask , jsonify  ,request ,make_response
# from flask_sqlalchemy import SQLAlchemy
# import uuid
# import datetime
# from functools import wraps

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Favour98@localhost/james'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

# db = SQLAlchemy(app)


# class User(db.Model):

#     """User model for authentication."""

#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.Integer(),unique=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=True)
#     admin = db.Column(db.Boolean, default=True)
#     Book= db.relationship('BookModel', backref='user', lazy='dynamic')


#     def json(self):
#         '''Display output as json object.'''

#         return {id: self.id, 'username': self.username,
#                 'password': self.password, 'admin': self.admin}


#     def __repr__(self):
#         return "<User(username='%s', email='%s')>" % (self.username,
#                                                       self.email)
# class BookCategory(db.Model):
#     """BookCtegory table defined """

#     __tablename__='BookCategorys'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     created_by = db.Column(db.String(64))
#     books = db.relationship('BookModel', backref='category',primaryjoin='BookCategory.id == BookModel.category_id',cascade="all, delete-orphan", lazy='dynamic')
    

#     def json(self):
#         ''' Display output as JSON object.'''

#         return {
#             "id": self.id,
#             "name": self.name,
#             "items_count": len(self.items.all()),
#             "created_at": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
#             "updated_at": self.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
#             "created_by": self.created_by,
#         }


# class BookModel(db.Model):

#     """BookModel defined."""

#     __tablename__ = 'BookModels'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80), nullable=False)
#     done = db.Column(db.Boolean, default=False, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     category_id = db.Column(db.Integer, db.ForeignKey('BookCategorys.id'))


    


#     def json(self):
#         ''' Display output as JSON object.'''

#         return {
#             "id": self.id,
#             "title": self.title,
#             "created_at": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
#             "updated_at": self.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
#             "done": self.done,
#         }