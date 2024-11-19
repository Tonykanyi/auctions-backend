from flask import Blueprint, request, jsonify
from flask.views import MethodView
from ..models import User
from .. import db
from ..utils import login_required  # Import from utils instead of auth_routes



user_blueprint = Blueprint('user', __name__)

class UserAPI(MethodView):

    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            password_hash=data['password_hash'],
            email=data['email'],
            role=data['role']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

user_blueprint.add_url_rule('/user', view_func=UserAPI.as_view('user'))
