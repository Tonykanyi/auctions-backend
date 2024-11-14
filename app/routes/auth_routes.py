from flask import Blueprint, request, jsonify
from flask.views import MethodView
from werkzeug.security import check_password_hash
from ..models import User
from .. import db
from ..utils import generate_token  # Import from utils

auth_blueprint = Blueprint('auth', __name__)

class LoginAPI(MethodView):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        token = generate_token(user)
        return jsonify({'token': token, 'role': user.role, 'message': 'Login successful'}), 200

auth_blueprint.add_url_rule('/login', view_func=LoginAPI.as_view('login'))
