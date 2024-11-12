from flask import Blueprint, request, jsonify, current_app
from flask.views import MethodView
from . import db
from .models import User, Item, Auction, Bid, Notification, Report, AuditLog
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
import jwt
from functools import wraps

# Utility function to create JWT token
def generate_token(user):
    payload = {
        'user_id': user.user_id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

# Authentication decorator
def login_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                if role and decoded_token['role'] != role:
                    return jsonify({'message': f'Access denied for {decoded_token["role"]} role'}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Blueprint definitions
auth_blueprint = Blueprint('auth', __name__)
user_blueprint = Blueprint('user', __name__)
item_blueprint = Blueprint('item', __name__)
auction_blueprint = Blueprint('auction', __name__)
bid_blueprint = Blueprint('bid', __name__)
notification_blueprint = Blueprint('notification', __name__)

### Authentication Routes ###
class LoginAPI(MethodView):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        token = generate_token(user)
        return jsonify({'token': token, 'role': user.role, 'message': 'Login successful'}), 200

auth_blueprint.add_url_rule('/login', view_func=LoginAPI.as_view('login'))

### User Routes ###
class UserAPI(MethodView):
    decorators = [login_required(role='admin')]

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

### Item Routes ###
class ItemAPI(MethodView):
    def post(self):
        data = request.get_json()
        new_item = Item(
            image_url=data['image_url'],
            title=data['title'],
            description=data['description'],
            starting_price=data['starting_price'],
            category=data['category'],
            posted_by=data['posted_by']
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item created successfully'}), 201

    def get(self):
        items = Item.query.all()
        return jsonify([{'item_id': item.item_id, 'title': item.title, 'description': item.description,
                         'image_url': item.image_url, 'starting_price': item.starting_price} for item in items])

item_blueprint.add_url_rule('/item', view_func=ItemAPI.as_view('item'))

### Auction Routes ###
class AuctionAPI(MethodView):
    decorators = [login_required(role='auctioneer')]

    def post(self):
        data = request.get_json()
        new_auction = Auction(
            item_id=data['item_id'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            status=data['status']
        )
        db.session.add(new_auction)
        db.session.commit()
        return jsonify({'message': 'Auction created successfully'}), 201

    def get(self):
        auctions = Auction.query.all()
        return jsonify([{'auction_id': auction.auction_id, 'item_id': auction.item_id, 'status': auction.status} for auction in auctions])

auction_blueprint.add_url_rule('/auction', view_func=AuctionAPI.as_view('auction'))

### Bid Routes ###
class BidAPI(MethodView):
    decorators = [login_required(role='bidder')]

    def post(self):
        data = request.get_json()
        new_bid = Bid(
            amount=data['amount'],
            bidder_id=data['bidder_id'],
            auction_id=data['auction_id']
        )
        db.session.add(new_bid)
        db.session.commit()
        return jsonify({'message': 'Bid created successfully'}), 201

bid_blueprint.add_url_rule('/bid', view_func=BidAPI.as_view('bid'))

### Notification Routes ###
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

# Registering all blueprints in your main Flask application file:
# app.register_blueprint(auth_blueprint, url_prefix='/auth')
# app.register_blueprint(user_blueprint, url_prefix='/users')
# app.register_blueprint(item_blueprint, url_prefix='/items')
# app.register_blueprint(auction_blueprint, url_prefix='/auctions')
# app.register_blueprint(bid_blueprint, url_prefix='/bids')
# app.register_blueprint(notification_blueprint, url_prefix='/notifications')
