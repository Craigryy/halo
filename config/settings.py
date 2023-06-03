from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#configuration 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Favour98@localhost/halo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'jesusislord'
port = 5000


#extension
db = SQLAlchemy(app)
