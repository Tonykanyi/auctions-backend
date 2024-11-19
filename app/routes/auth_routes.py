from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from .. import db
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token  # Use JWT for token generation

auth_blueprint = Blueprint('auth', __name__)

# Login API
@auth_blueprint.route('/login', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type', 'Authorization'])
def login():
    try:
        data = request.get_json()
        current_app.logger.debug(f"Received data: {data}")  # Use current_app for logging

        if not data:
            return jsonify({'message': 'Invalid input: No data received'}), 400

        username = str(data.get('username', '')).strip()
        password = str(data.get('password', '')).strip()

        current_app.logger.debug(f"username: {username} (type: {type(username)})")
        current_app.logger.debug(f"password: {password} (type: {type(password)})")

        if not username or not password:
            return jsonify({'message': 'Invalid input: Username and password are required'}), 400

        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'message': 'Invalid username or password'}), 401

        # Generate JWT token
        token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify({'token': token, 'role': user.role, 'message': 'Login successful'}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        current_app.logger.error(f"Error during login: {str(e)}")
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

# Registration API
@auth_blueprint.route('/register', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type', 'Authorization'])
def register():
    try:
        data = request.get_json()
        current_app.logger.debug(f"Received registration data: {data}")

        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            return jsonify({'message': 'Invalid input'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already taken'}), 409
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already registered'}), 409

        password_hash = generate_password_hash(data['password'])
        new_user = User(
            username=data['username'],
            password_hash=password_hash,
            email=data['email'],
            role=data.get('role', 'client')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        current_app.logger.error(f"Error during registration: {str(e)}")
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
