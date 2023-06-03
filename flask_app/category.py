'''Script for BookCategory  Api Accesspoint. '''

from flask import jsonify, request, make_response
from flask_app.model import BookCategory, app, db
from flask_app.authenticate import token_required


# Write a function named `test` which returns a json object with the mesage: "test route ",
# and assign to the static route of ('/test')
@app.route('/test', methods=['GET'])
def test():
    '''Test route'''
    return make_response(jsonify({'message': 'test route'}), 200)


# Write a function named "addnew_category`which creates new book category using `POST` method,
# and assign to the static route of ('/categories/')
@app.route("/categories/", methods=['POST'])
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

# Write a function named `list which updates an existing book using `DELETE` method,
# and assign to the static route of ('/categories/<int:id>')


@app.route('/categories/', methods=['GET'])
@token_required
def list_book_category(current_user):
    '''list all category for a book.'''
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    categories = BookCategory.query.all()

    return make_response(jsonify([category.to_json() for category in categories]), 200)

# Write a function named `get` which query the database for an existing book using `GET` method,
# and assign to the static route of ('/categories/<int:id>')


@app.route('/categories/<int:id>', methods=['GET'])
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

# Write a function named `update` which updates an existing book using `PUT` method,
# and assign to the static route of ('/categories/<int:id>')


@app.route("/categories/<int:id>", methods=['PUT'])
@token_required
def update(current_user, id):
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


# Write a function named `delete` which updates an existing book using `DELETE` method,
# and assign to the static route of ('/categories/<int:id>')
@app.route("/categories/<int:id>", methods=['DELETE'])
@token_required
def delete(current_user, id):
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
