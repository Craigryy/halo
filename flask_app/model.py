"""Class decorator defined for the Model Scripts."""

from config import db

class Base(db.Model):
    """
    Abstract Base class used to define id.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        """
        Save the object to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):

        """
        Delete the object from the database.
        """
        db.session.add(self)
        db.session.delete(self)
        db.session.commit()


class User(Base):
    """
    User model for authentication.
    """
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    # Establishing the relationship
    category = db.relationship("BookCategory", backref="owner", lazy="dynamic")

    def to_json(self):
  
        """
        Convert User object to a JSON representation.
        """
        return {
            "id": self.id,
            "name": self.name,
            "public_id": self.public_id,
            "password": self.password,
            "admin": self.admin,
        }


class BookCategory(Base):

    """
    BookCategory table defined.
    """
    __tablename__ = "BookCategorys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.String(100))
    # Linking back to User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    books = db.relationship(
        "BookModel", backref="category", cascade="all, delete-orphan", lazy="dynamic"
    )

    def to_json(self):

        """
        Convert BookCategory object to a JSON representation.
        """

        return {"id": self.id, "name": self.name, "created_by": self.created_by}


class BookModel(Base):

    """
    BookModel defined.
    """

    __tablename__ = "BookModels"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey("BookCategorys.id"))

    def to_json(self):
        """
        Convert BookModel object to a JSON representation.
        """
        return {"id": self.id, "title": self.title, "author": self.author}

