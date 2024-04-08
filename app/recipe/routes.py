import json

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.auth.models import User
from app.recipe.models import Recipe
from app.utils import FieldValidator

recipe_bp = Blueprint('recipe_bp', __name__)

@recipe_bp.route('/recipes', methods=['POST'])
@jwt_required()
def create_recipe():
    """
    Create a new recipe.

    Requires authentication via JWT token.

    Returns:
        JSON response containing the created recipe information.
    """
    data = request.json
    title = data.get('title')
    description = data.get('description')
    instructions = data.get('instructions')
    ingredients = data.get('ingredients')  # List of ingredients with quantities

    # Check if all required fields are present in the request
    required_fields = ['title', 'ingredients']
    error_response, status_code = FieldValidator.check_required_fields(data, required_fields)
    if error_response:
        return jsonify(error_response), status_code

    # Get the ID of the logged-in user
    current_user_id = get_jwt_identity()

    # Check if the user exists
    user = User.get_data(id=current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Convert ingredients to JSON format
    ingredients_json = json.dumps(ingredients)

    # Create a new recipe associated with the logged-in user
    new_recipe = Recipe.create(title=title, description=description, instructions=instructions,
                               created_by=current_user_id, ingredients=ingredients_json)

    response = {
        'status': 'success',
        'message': 'Recipe created successfully',
        'data': {
            'recipe': new_recipe.title
        }
    }
    return jsonify(response), 201

@recipe_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
@jwt_required()
def get_recipe(recipe_id):
    """
    Get recipe details by ID.

    Requires authentication via JWT token.

    Args:
        recipe_id (int): The ID of the recipe to retrieve.

    Returns:
        JSON response containing the recipe information.
    """
    recipe = Recipe.get_data(id=recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    return jsonify({
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'created_by': recipe.created_by
    }), 200


@recipe_bp.route('/recipes/search', methods=['GET'])
@jwt_required()
def search_recipes():
    query = request.args.get('q')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    recipes = Recipe.get_paginated_search(query, page=page, per_page=per_page)
    recipes_data = []
    for recipe in recipes:
        recipes_data.append({
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'created_by': recipe.created_by
        })
    return jsonify(recipes_data), 200


@recipe_bp.route('/recipes/<int:recipe_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_recipe(recipe_id):
    """
    Update recipe details by ID.

    Requires authentication via JWT token.

    Args:
        recipe_id (int): The ID of the recipe to update.

    Returns:
        JSON response indicating success or failure of the update operation.
    """
    data = request.json
    recipe = Recipe.get_data(id=recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    # Update the recipe fields
    recipe.update(data)
    return jsonify({'message': 'Recipe updated successfully'}), 200

@recipe_bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    """
    Delete recipe by ID.

    Requires authentication via JWT token.

    Args:
        recipe_id (int): The ID of the recipe to delete.

    Returns:
        JSON response indicating success or failure of the delete operation.
    """
    recipe = Recipe.get_data(id=recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    recipe.delete()
    return jsonify({'message': 'Recipe deleted successfully'}), 200
