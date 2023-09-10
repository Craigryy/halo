from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import BookCategory, db

category_app = Blueprint('category_app', __name__)

# @category_app.route('/', methods=['GET'])
# def test():
#     """
#     A test route.
#     """
#     return make_response(jsonify({'message': 'test route'}), 200)

@category_app.route('/categories/add', methods=['POST'])
@jwt_required()
def add_new_book_category():
    """
    Create a new book category.
    """
    json_data = request.get_json()
    name, created_by = json_data['name'], json_data['created_by']
    category = BookCategory(name=name, created_by=created_by)
    category.save()

    return jsonify({'BookCategory': category.to_json()})

@category_app.route('/categories/', methods=['GET'])
@jwt_required()
def list_book_categories():
    """
    List all book categories.
    """
    categories = BookCategory.query.all()
    return make_response(jsonify([category.to_json() for category in categories]), 200)

@category_app.route('/categories/<int:id>', methods=['GET'])
@jwt_required()
def get_book_category_by_id(id):
    """
    Get a single book category by ID.
    """
    try:
        category = BookCategory.query.filter_by(id=id).first()
        if category:
            return make_response(jsonify({'category': category.to_json()}), 200)
        return make_response(jsonify({'message': 'Category not found'}), 404)
    except Exception as e:
        error_message = f"Error getting category: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)

@category_app.route('/categories/<int:id>/', methods=['PUT'])
@jwt_required()
def update_book_category(id):
    """
    Update a book category.
    """
    try:
        category = BookCategory.query.filter_by(id=id).first()
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

@category_app.route('/categories/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_book_category(id):
    """
    Delete a book category by ID.
    """
    try:
        book_category = BookCategory.query.filter_by(id=id).first()
        if book_category:
            book_category.delete()
            return jsonify({'message': 'Category deleted successfully'})
        return make_response(jsonify({'message': 'Category not found'}), 404)
    except Exception as e:
        error_message = f"Error deleting category: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)
