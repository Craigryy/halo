from flask import Blueprint, jsonify, make_response, request

from .authenticate import token_required
from .model import BookCategory, BookModel

book_app = Blueprint('book_app', __name__)

@book_app.route('/categories/<int:id>/books/', methods=['POST'])
@token_required
def create_book(current_user, id):
    """Create a book in the specified category."""
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    category = BookCategory.query.filter_by(id=id, user_id=current_user.id).first()
    if not category:
        return make_response(jsonify({'message': 'Category with id:{} was not found'.format(id)}))

    json_data = request.get_json()
    title, author = json_data['title'], json_data['author']
    book = BookModel(title=title, author=author)
    book.category_id = category.id
    book.save()

    return jsonify({'book': book.to_json()})


@book_app.route('/categories/<int:id>/books/<int:book_id>', methods=['PUT'])
@token_required
def update_book(current_user, id, book_id):
    """Update a book in the specified category."""
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    category = BookCategory.query.filter_by(id=id).first()
    if not category:
        return make_response(jsonify({'message': 'Category with id:{} was not found'.format(id)}))

    book = BookModel.query.get(book_id)
    if not book:
        return make_response(jsonify({'message': 'Book with id:{} was not found'.format(book_id)}))

    book.title = request.json.get('title', book.title)
    book.author = request.json.get('author', book.author)
    book.category_id = request.json.get('category_id', book.category_id)
    book.category_id = category.id
    book.save()

    return make_response(jsonify({"message": "Book updated successfully", "book": book.to_json()}), 200)


@book_app.route('/categories/<int:id>/books/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user, id, book_id):
    """Delete a book from the specified category."""
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    book_category = BookCategory.query.filter_by(id=id, user_id=current_user.id).first()
    if not book_category:
        return make_response(jsonify({'message': 'Book category with id:{} was not found'.format(book_id)}))

    book = BookModel.query.get(book_id)
    if not book:
        return make_response(jsonify({'message': 'Book with id:{} was not found'.format(book_id)}))

    book.delete()
    return make_response(jsonify({"message": "Book deleted successfully"}), 200)
