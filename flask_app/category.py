'''Script for BookCategory  Api Accesspoint. '''

from flask import jsonify, request, make_response,Blueprint,app
from .model import BookCategory,db
from .authenticate import token_required
from flasgger import swag_from

category_app = Blueprint('category_app', __name__)


# Write a function named `test` which returns a json object
#  with the mesage: "test route ",
# and assign to the static route of ('/test')
@category_app.route('/', methods=['GET'])
# @swag_from('swagger/test.yml')
def test():
    '''Test route'''
    return make_response(jsonify({'message': 'test route'}), 200)


# Write a function named "addnew_category`which creates new book 
# category using `POST` method, and assign to the static route of
#  ('/categories/')
@category_app.route("/categories/", methods=['POST'])
# @swag_from('swagger/adnew_bookcategory.yml')
@token_required
def addnew_bookcategory(current_user):
    ''' create a book in the category. '''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    json_data = request.get_json()
    name, created_by = json_data['name'], json_data['created_by']
    category = BookCategory(
        name=name, created_by=created_by, user_id=current_user.id)
    category.save()

    return jsonify({'BookCategory': category.to_json})

# Write a function named `list which updates an existing book 
# using `DELETE` method,and assign to the static route of
#  ('/categories/<int:id>')


@category_app.route('/categories/', methods=['GET'])
# @swag_from('swagger/list_book_category.yml')
@token_required
def list_book_category(current_user):
    '''list all category for a book.'''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    categories = BookCategory.query.all()

    return make_response(jsonify([category.to_json() for category in categories]), 200)

# Write a function named `get` which query the database
#  for an existing book using `GET` method, and assign
#  to the static route of ('/categories/<int:id>')


@category_app.route('/categories/<int:id>', methods=['GET'])
# @swag_from('swagger/get_book_category.yml')
@token_required
def get_book_category(current_user, id):
    '''Get a single book category.'''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        category = BookCategory.query.filter_by(
            id=id, user_id=current_user.id).first()
        if category:
            return make_response(jsonify({'category': category.to_json()}), 200)
        return make_response(jsonify({'message': 'category not found'}), 404)
    except Exception as e:
        error_message = f"Error getting category: {str(e)}"
    return make_response(jsonify({'message': error_message}), 500)

# Write a function named `update` which updates an existing book
#  using `PUT` method, and assign to the static route of
#  ('/categories/<int:id>')


@category_app.route("/categories/<int:id>", methods=['PUT'])
# @swag_from('swagger/update_book_category.yml')
@token_required
def update_book_category(current_user, id):
    '''Update a book category. '''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        category = BookCategory.query.filter_by(
            id=id, user_id=current_user.id).first()
        if category:
            data = request.get_json()
            category.name = data['name']
            category.created_by = data['created_by']
            db.session.commit()
            return make_response(jsonify({'message': 'category updated'}), 200)
        return make_response(jsonify({'message': 'category not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating category'}.format(e)), 500)

# Write a function named `delete` which updates an existing book 
# using `DELETE` method, and assign to the static route of 
# ('/categories/<int:id>')

@category_app.route("/categories/<int:id>", methods=['DELETE'])
# @swag_from('swagger/delete_category.yml')
@token_required
def delete_category(current_user, id):
    '''Delete a book category. '''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        book = BookCategory.query.filter_by(
            id=id, user_id=current_user.id).first()
        if book:
            book.delete()
            return jsonify({'message': 'category successfully deleted'})
        return make_response(jsonify({'message': 'category not found'}), 404)
    except Exception as e:
        error_message = f"Error deleting category: {str(e)}"
    return make_response(jsonify({'message': error_message}), 500)
