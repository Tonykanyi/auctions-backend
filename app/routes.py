from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import User, Item, Auction, Bid, BidHistory, Report, AuditLog, Notification
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
import jwt
from functools import wraps

routes = Blueprint('routes', __name__)

# Utility function to create a JWT token
def generate_token(user):
    payload = {
        'user_id': user.user_id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

# Decorator to require authentication and check roles
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

# Login route
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    token = generate_token(user)
    return jsonify({'token': token, 'role': user.role, 'message': 'Login successful'}), 200

# User Routes
@routes.route('/user', methods=['POST'])
@login_required(role='admin')
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'password_hash', 'email', 'role')):
        return jsonify({'message': 'Missing required fields'}), 400

    new_user = User(
        username=data['username'],
        password_hash=data['password_hash'],
        email=data['email'],
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Item Routes
@routes.route('/item', methods=['POST'])
@login_required(role='admin')  # Adjust role as per your requirements
def create_item():
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

@routes.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'item_id': item.item_id, 'title': item.title, 'description': item.description, 'image_url':item.image_url, 'starting_price': item.starting_price} for item in items])

# Auction Routes
@routes.route('/auction', methods=['POST'])
@login_required(role='auctioneer')
def create_auction():
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

@routes.route('/auctions', methods=['GET'])
def get_auctions():
    auctions = Auction.query.all()
    return jsonify([{'auction_id': auction.auction_id, 'item_id': auction.item_id, 'status': auction.status} for auction in auctions])

# Bid Routes
@routes.route('/bid', methods=['POST'])
@login_required(role='bidder')
def create_bid():
    data = request.get_json()
    new_bid = Bid(
        amount=data['amount'],
        bidder_id=data['bidder_id'],
        auction_id=data['auction_id']
    )
    db.session.add(new_bid)
    db.session.commit()
    return jsonify({'message': 'Bid created successfully'}), 201

# Notification Routes
@routes.route('/notification', methods=['POST'])
def create_notification():
    data = request.get_json()
    new_notification = Notification(
        message=data['message'],
        user_id=data['user_id']
    )
    db.session.add(new_notification)
    db.session.commit()
    return jsonify({'message': 'Notification sent successfully'}), 201

@routes.route('/notifications/<int:bidder_id>', methods=['GET'])
def get_notifications(bidder_id):
    notifications = Notification.query.filter_by(user_id=bidder_id).all()
    return jsonify([{'notification_id': notification.notification_id, 'message': notification.message} for notification in notifications])

# Report and Audit Log routes follow similar patterns...

# Error Handling (Example)
@routes.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404
