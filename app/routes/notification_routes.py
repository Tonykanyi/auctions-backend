from flask import Blueprint, request, jsonify
from flask.views import MethodView
from ..models import Notification
from .. import db

notification_blueprint = Blueprint('notification', __name__)

class NotificationAPI(MethodView):
    def post(self):
        data = request.get_json()
        new_notification = Notification(
            message=data['message'],
            user_id=data['user_id']
        )
        db.session.add(new_notification)
        db.session.commit()
        return jsonify({'message': 'Notification sent successfully'}), 201

notification_blueprint.add_url_rule('/notification', view_func=NotificationAPI.as_view('notification'))
