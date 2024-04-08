from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required)

from app import db
from app.auth.models import User
from app.utils import FieldValidator

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.json

    # Check required fields
    required_fields = ['username', 'password']
    error_response, status_code = FieldValidator.check_required_fields(data, required_fields)
    if error_response:
        return jsonify(error_response), status_code

    username = data.get('username')
    password = data.get('password')

    # Retrieve the user by username
    user = User.get_data(username=username)

    # Check if the user exists and if the password is correct
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        response = {
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }
        return jsonify(response), 200
    else:
        # Invalid username or password
        response = {
            'status': 'error',
            'message': 'Invalid username or password'
        }
        return jsonify(response), 401

@auth.route('/register', methods=['POST'])
def register():
    data = request.json

    # Check if all required fields are present in the request
    required_fields = ['username', 'password', 'name']
    error_response, status_code = FieldValidator.check_required_fields(data, required_fields)
    if error_response:
        return jsonify(error_response), status_code

    username = data.get('username')
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    password = data.get('password')

    # Check if the username already exists
    if User.get_data(username=username):
        response = {
            'status': 'error',
            'message': 'Username already exists.'
        }
        return jsonify(response), 409

    # Create a new user
    new_user = User(username=username, name=name, phone=phone, email=email)
    new_user.set_password(password)
    db.session.add(new_user)  # Add the new user to the session
    db.session.commit()

    response = {
        'status': 'success',
        'message': 'Registration successful',
        'data': {
            'username': new_user.username
        }
    }

    return jsonify(response), 200


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    response = {
        'status': 'success',
        'message': 'Access token refreshed',
        'access_token': new_access_token
    }
    return jsonify(response), 200