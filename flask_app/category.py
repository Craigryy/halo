from flask import Blueprint, jsonify, make_response, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import BookCategory, db ,User
from flask_app.authenticate import auth_app  


category_app = Blueprint('category_app', __name__)


@category_app.route('/categories/admin', methods=['GET'])
@jwt_required()
def list_book_category():
    """
    List all book categories.
    """

    categories = BookCategory.query.all()

    return make_response(jsonify([category.to_json() for category in categories]), 200)



@category_app.route('/categories/add', methods=['POST'])
@jwt_required()
def add_new_book_category():
    """
    Create a new book category.
    """
    json_data = request.get_json()
    name, created_by = json_data['name'], json_data['created_by']
    
    # Get the user ID of the currently authenticated user
    current_user_id = get_jwt_identity()
    
    # Query the currently logged-in user based on their public_id
    current_user = User.query.filter_by(public_id=current_user_id).first()
    
    if current_user:
        # Create the category associated with the current user
        category = BookCategory(name=name, created_by=created_by, user_id=current_user.id)
        category.save()

        return jsonify({'BookCategory': category.to_json()})
    return make_response(jsonify({'message': 'User not found'}), 404)

@category_app.route('/categories/', methods=['GET'])
@jwt_required()
def list_book_categories():
    """
    List all book categories belonging to the currently authenticated user.
    """
    try:
        # Get the user ID of the currently authenticated user
        current_user_id = get_jwt_identity()
        
        # Query the currently logged-in user based on their public_id
        current_user = User.query.filter_by(public_id=current_user_id).first()

        if current_user:
            # Retrieve only the categories owned by the current user
            categories = BookCategory.query.filter_by(user_id=current_user.id).all()
            
            return make_response(jsonify([category.to_json() for category in categories]), 200)
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        error_message = f"Error listing categories: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)

@category_app.route('/categories/<int:id>', methods=['GET'])
@jwt_required()
def get_book_category_by_id(id):
    """
    Get a single book category by ID, but only if it belongs to the currently authenticated user.
    """
    try:
        # Get the user ID of the currently authenticated user
        current_user_id = get_jwt_identity()
        
        # Query the currently logged-in user based on their public_id
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if current_user:
            # Retrieve the category only if it belongs to the current user
            category = BookCategory.query.filter_by(id=id, user_id=current_user.id).first()
            if category:
                return make_response(jsonify({'category': category.to_json()}), 200)
            return make_response(jsonify({'message': 'Category not found or unauthorized'}), 404)
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        error_message = f"Error getting category: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)

@category_app.route('/categories/<int:id>/', methods=['PUT'])
@jwt_required()
def update_book_category(id):
    """
    Update a book category, but only if it belongs to the currently authenticated user.
    """
    try:
        # Get the user ID of the currently authenticated user
        current_user_id = get_jwt_identity()
        
        # Query the currently logged-in user based on their public_id
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if current_user:
            # Retrieve the category only if it belongs to the current user
            category = BookCategory.query.filter_by(id=id, user_id=current_user.id).first()
            if category:
                data = request.get_json()
                category.name = data['name']
                category.created_by = data['created_by']
                db.session.commit()
                return make_response(jsonify({'message': 'Category updated successfully'}), 200)
            return make_response(jsonify({'message': 'Category not found or unauthorized'}), 404)
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        error_message = f"Error updating category: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)

@category_app.route('/categories/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_book_category(id):
    """
    Delete a book category by ID, but only if it belongs to the currently authenticated user.
    """
    try:
        # Get the user ID of the currently authenticated user
        current_user_id = get_jwt_identity()
        
        # Query the currently logged-in user based on their public_id
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if current_user:
            # Retrieve the category only if it belongs to the current user
            category = BookCategory.query.filter_by(id=id, user_id=current_user.id).first()
            if category:
                category.delete()
                return jsonify({'message': 'Category deleted successfully'})
            return make_response(jsonify({'message': 'Category not found or unauthorized'}), 404)
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        error_message = f"Error deleting category: {str(e)}"
        return make_response(jsonify({'message': error_message}), 500)
