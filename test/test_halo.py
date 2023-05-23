import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Favour98@localhost/james'  # PostgreSQL URI
db = SQLAlchemy(app)

# Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, title, author, category_id):
        self.title = title
        self.author = author
        self.category_id = category_id

# Unit tests
class ModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Favour98@localhost/james'  # PostgreSQL URI
        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_category(self):
        category = Category('Fiction')
        db.session.add(category)
        db.session.commit()

        self.assertIsInstance(category.id, int)
        self.assertGreater(category.id, 0)

    def test_book(self):
        category = Category('Fiction')
        db.session.add(category)
        db.session.commit()

        book = Book('Book Title', 'Author Name', category.id)
        db.session.add(book)
        db.session.commit()

        self.assertIsInstance(book.id, int)
        self.assertGreater(book.id, 0)
        self.assertEqual(book.category_id, category.id)

if __name__ == '__main__':
    unittest.main()
