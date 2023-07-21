from flask import Blueprint, jsonify, make_response, request

from .authenticate import token_required
from .model import BookCategory, db

category_app = Blueprint('category_app', __name__)

@category_app.route('/', methods=['GET'])
def test():
    """A test route."""
    return make_response(jsonify({'message': 'test route'}), 200)


@category_app.route("/categories/", methods=['POST'])
@token_required
def addnew_bookcategory(current_user):
    """Create a new book category."""
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    json_data = request.get_json()
    name, created_by = json_data['name'], json_data['created_by']
    category = BookCategory(name=name, created_by=created_by, user_id=current_user.id)
    category.save()

    return jsonify({'BookCategory': category.to_json()})


@category_app.route('/categories/', methods=['GET'])
@token_required
def list_book_category(current_user):
    """List all book categories."""
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    categories = BookCategory.query.all()

    return make_response(jsonify([category.to_json() for category in categories]), 200)


@category_app.route('/categories/<int:id>', methods=['GET'])
@token_required
def get_book_category(current_user, id):
    """Get a single book category by ID."""
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        category = BookCategory.query.filter_by(id=id, user_id=current_user.id).first()
        if category:
            return make_response(jsonify({'category': category.to_json()}), 200)
        return make_response(jsonify({'message': 'Category not found'}), 404)
    except Exception as e:
        error_message = f"Error getting category: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)


@category_app.route("/categories/<int:id>", methods=['PUT'])
@token_required
def update(current_user, id):
    """Update a book category."""
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        category = BookCategory.query.filter_by(id=id, user_id=current_user.id).first()
        if category:
            data = request.get_json()
            category.name = data['name']
            category.created_by = data['created_by']
            db.session.commit()
            return make_response(jsonify({'message': 'Category updated successfully'}), 200)
        return make_response(jsonify({'message': 'Category not found'}), 404)
    except Exception as e:
        error_message = f"Error updating category: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)


@category_app.route("/categories/<int:id>", methods=['DELETE'])
@token_required
def delete(current_user, id):
    """Delete a book category by ID."""
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    try:
        book_category = BookCategory.query.filter_by(id=id, user_id=current_user.id).first()
        if book_category:
            book_category.delete()
            return jsonify({'message': 'Category deleted successfully'})
        return make_response(jsonify({'message': 'Category not found'}), 404)
    except Exception as e:
        error_message = f"Error deleting category: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)
