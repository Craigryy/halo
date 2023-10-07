"""Class decorator defined for the Model Scripts."""

from config import db

<<<<<<< HEAD
class Base(db.Model):
    """
    Abstract Base class used to define id.
    """
=======

class Base(db.Model):
    """Abstract Base class used to define id."""
>>>>>>> origin/master

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
<<<<<<< HEAD
        """
        Save the object to the database.
        """
=======
        """Save the object to the database."""
>>>>>>> origin/master
        db.session.add(self)
        db.session.commit()

    def delete(self):
<<<<<<< HEAD
        """
        Delete the object from the database.
        """
=======
        """Delete the object from the database."""
>>>>>>> origin/master
        db.session.add(self)
        db.session.delete(self)
        db.session.commit()


class User(Base):
<<<<<<< HEAD
    """
    User model for authentication.
    """
=======
    """User model for authentication."""
>>>>>>> origin/master

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    category = db.relationship("BookCategory", backref="owner", lazy="dynamic")

    def to_json(self):
<<<<<<< HEAD
        """
        Convert User object to a JSON representation.
        """
=======
        """Convert User object to a JSON representation."""
>>>>>>> origin/master
        return {
            "id": self.id,
            "name": self.name,
            "public_id": self.public_id,
            "password": self.password,
            "admin": self.admin,
        }


class BookCategory(Base):
<<<<<<< HEAD
    """
    BookCategory table defined.
    """
=======
    """BookCategory table defined."""
>>>>>>> origin/master

    __tablename__ = "BookCategorys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    books = db.relationship(
        "BookModel", backref="category", cascade="all, delete-orphan", lazy="dynamic"
    )

    def to_json(self):
<<<<<<< HEAD
        """
        Convert BookCategory object to a JSON representation.
        """
=======
        """Convert BookCategory object to a JSON representation."""
>>>>>>> origin/master
        return {"id": self.id, "name": self.name, "created_by": self.created_by}


class BookModel(Base):
<<<<<<< HEAD
    """
    BookModel defined.
    """
=======
    """BookModel defined."""
>>>>>>> origin/master

    __tablename__ = "BookModels"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey("BookCategorys.id"))

    def to_json(self):
<<<<<<< HEAD
        """
        Convert BookModel object to a JSON representation.
        """
        return {"id": self.id, "title": self.title, "author": self.author}

=======
        """Convert BookModel object to a JSON representation."""
        return {"id": self.id, "title": self.title, "author": self.author}
>>>>>>> origin/master
