from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required ,get_jwt_identity
from .model import BookCategory, BookModel, User

book_app = Blueprint('book_app', __name__)

@book_app.route('/categories/<int:id>/books/', methods=['GET', 'POST'])
@jwt_required()
def create_book(id):
    """
    Create a book in the specified category.
    """
    category = BookCategory.query.filter_by(id=id).first()
    if not category:
        return make_response(jsonify({'message': 'Category with id:{} was not found'.format(id)}))

    json_data = request.get_json()
    title, author = json_data['title'], json_data['author']
    book = BookModel(title=title, author=author)
    book.category_id = category.id
    book.save()

    return jsonify({'book': book.to_json()})


@book_app.route('/categories/<int:id>/books/', methods=['GET'])
@jwt_required()
def get_books_by_category(id):
    """
    Get books in the specified category.
    """
    try:
        category = BookCategory.query.get(id)
        if not category:
            return make_response(jsonify({'message': 'Category not found'}), 404)

        books = BookModel.query.filter_by(category_id=id).all()

        books_data = []
        for book in books:
            book_data = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'category_id': book.category_id,
            }
            books_data.append(book_data)

        return jsonify(books_data)

    except Exception as e:
        error_message = f"Error fetching books: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)


@book_app.route('/categories/<int:category_id>/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book_and_category(category_id, book_id):
    """
    Get a particular book and its category.
    """
    category = BookCategory.query.filter_by(id=category_id).first()
    if not category:
        return make_response(jsonify({'message': 'Category with id:{} was not found'.format(category_id)}))

    book = BookModel.query.get(book_id)
    if not book:
        return make_response(jsonify({'message': 'Book with id:{} was not found'.format(book_id)}))

    book_data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category': category.name
    }

    return jsonify({'book': book_data})


@book_app.route('/books/', methods=['GET'])
@jwt_required()
def get_books_by_user():
    """
    Get books owned by the currently authenticated user.
    """
    try:
        # Get the user ID of the currently authenticated user
        current_user_id = get_jwt_identity()

        # Query the currently logged-in user based on their public_id
        current_user = User.query.filter_by(public_id=current_user_id).first()

        if current_user:
            # Retrieve only the books owned by the current user
            books = BookModel.query.filter_by(user_id=current_user.id).all()
            books_data = []

            for book in books:
                category = BookCategory.query.get(book.category_id)
                if not category:
                    category_name = None
                else:
                    category_name = category.name

                book_data = {
                    'id': book.id,
                    'title': book.title,
                    'author': book.author,
                    'category_id': book.category_id,
                    'category_name': category_name,
                }
                books_data.append(book_data)

            return jsonify(books_data)
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)

    except Exception as e:
        error_message = f"Error fetching books: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)


# @book_app.route('/books/', methods=['GET'])
# @jwt_required()
# def get_all_books():
#     """
#     Get all books.
#     """
#     try:
#         books = BookModel.query.all()
#         books_data = []

#         for book in books:
#             category = BookCategory.query.get(book.category_id)
#             if not category:
#                 category_name = None
#             else:
#                 category_name = category.name

#             book_data = {
#                 'id': book.id,
#                 'title': book.title,
#                 'author': book.author,
#                 'category_id': book.category_id,
#                 'category_name': category_name,
#             }
#             books_data.append(book_data)

#         return jsonify(books_data)

#     except Exception as e:
#         error_message = f"Error fetching books: {str(e)}"
#         return make_response(jsonify({'message': error_message}), 500)

@book_app.route('/categories/<int:id>/books/<int:book_id>/', methods=['PUT'])
@jwt_required()
def update_book(id, book_id):
    """
    Update a book in the specified category.
    """
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
@jwt_required()
def delete_book(id, book_id):
    """
    Delete a book from the specified category.
    """
    book_category = BookCategory.query.filter_by(id=id).first()
    if not book_category:
        return make_response(jsonify({'message': 'Book category with id:{} was not found'.format(book_id)}))

    book = BookModel.query.get(book_id)
    if not book:
        return make_response(jsonify({'message': 'Book with id:{} was not found'.format(book_id)}))

    book.delete()
    return make_response(jsonify({"message": "Book deleted successfully"}), 200)