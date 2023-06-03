from flask import jsonify, request, make_response
from flask_app.model import BookModel, BookCategory, app
from flask_app.authenticate import token_required

# Create book


@app.route('/categories/<int:id>/books/', methods=['POST'])
@token_required
def create_book(current_user, id):
    '''Create a book. '''
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    category = BookCategory.query.filter_by(
        id=id, user_id=current_user.id).first()
    if not category:
        return make_response(jsonify(('category with id:{} was not found' .format(id))))
    json_data = request.get_json()
    title, author = json_data['title'], json_data['author']
    book = BookModel(title=title, author=author)
    book.category_id = category.id
    book.save()

    return jsonify({'book': book.to_json})


# Write a function named `update_book` which updates an existing book using `PUT` method,
# and assign to the static route of ('/categories/<int:id>/books/<int:book_id>')
@app.route('/categories/<int:id>/books/<int:book_id>', methods=['PUT'])
@token_required
def update_book(current_user, id, book_id):
    '''Update a book. '''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    category = BookCategory.query.filter_by(id=id).first()

    if not category:
        return make_response(('bucket list with id:{} was not found' .format(id)))

    book = BookModel.query.get(id)
    if not book:
        return make_response(('book with id:{} was not found' .format(book_id)))

    book = BookModel.query.get(id)
    if book:
        book.title = request.json.get('title', book.title)
        book.author = request.json.get('author', book.author)
        book.category_id = request.json.get('category_id', book.category_id)
        book.category_id = category.id
        book.save()
        return make_response(jsonify({"message": "Book updated successfully", "book": book.to_json()}), 200)

    return make_response(jsonify({"message": "Book not found"}), 404)


# Write a function named `delete_book` which updates an existing book using `DELETE` method,
# and assign to the static route of ('/categories/<int:id>/books/<int:book_id>'')
@app.route('/categories/<int:id>/books/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user, id, book_id):
    '''Delete a book in a category '''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    bookcategory = BookCategory.query.filter_by(
        id=id, user_id=current_user.id).first()

    if not bookcategory:
        return make_response(('book category with id:{} was not found' .format(book_id)))

    book = BookModel.query.get(id)
    if book:
        book.delete()
        return make_response(jsonify({"message": "Book deleted successfully"}), 200)

    return make_response(jsonify({"message": "Book not found"}), 404)
