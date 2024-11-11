from flask import Blueprint, request, jsonify
from . import db
from .models import PlatformOwner, AuctionCompany, Item, Auction, Bid, Bidder, BidHistory, Report, AuditLog, Notification
from datetime import datetime

routes = Blueprint('routes', __name__)

# PlatformOwner Routes
@routes.route('/platform_owner', methods=['POST'])
def create_platform_owner():
    data = request.get_json()
    new_owner = PlatformOwner(
        username=data['username'],
        password_hash=data['password_hash'],
        email=data['email']
    )
    db.session.add(new_owner)
    db.session.commit()
    return jsonify({'message': 'Platform owner created successfully'}), 201

# AuctionCompany Routes
@routes.route('/auction_company', methods=['POST'])
def create_auction_company():
    data = request.get_json()
    new_company = AuctionCompany(
        name=data['name'],
        contact_email=data['contact_email']
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': 'Auction company created successfully'}), 201

@routes.route('/auction_company', methods=['GET'])
def get_auction_companies():
    companies = AuctionCompany.query.all()
    return jsonify([{'company_id': company.company_id, 'name': company.name, 'contact_email': company.contact_email} for company in companies])

# Item Routes
@routes.route('/item', methods=['POST'])
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
    return jsonify([{'item_id': item.item_id, 'title': item.title, 'description': item.description, 'starting_price': item.starting_price} for item in items])

# Auction Routes
@routes.route('/auction', methods=['POST'])
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

# Bidder Routes
@routes.route('/bidder', methods=['POST'])
def create_bidder():
    data = request.get_json()
    new_bidder = Bidder(
        username=data['username'],
        password_hash=data['password_hash'],
        email=data['email']
    )
    db.session.add(new_bidder)
    db.session.commit()
    return jsonify({'message': 'Bidder created successfully'}), 201

@routes.route('/bidders', methods=['GET'])
def get_bidders():
    bidders = Bidder.query.all()
    return jsonify([{'bidder_id': bidder.bidder_id, 'username': bidder.username} for bidder in bidders])

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

# Report Routes
@routes.route('/report', methods=['POST'])
def create_report():
    data = request.get_json()
    new_report = Report(
        report_type=data['report_type'],
        generated_by=data['generated_by']
    )
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'message': 'Report generated successfully'}), 201

# AuditLog Routes
@routes.route('/audit_log', methods=['POST'])
def create_audit_log():
    data = request.get_json()
    new_log = AuditLog(
        action=data['action'],
        user_id=data['user_id']
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Audit log created successfully'}), 201
