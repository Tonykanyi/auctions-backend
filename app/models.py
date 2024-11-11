# app/models.py

from . import db
from datetime import datetime

class PlatformOwner(db.Model):
    __tablename__ = 'platform_owners'
    owner_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuctionCompany(db.Model):
    __tablename__ = 'auction_companies'
    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('auction_companies.company_id'), nullable=False)

class Auction(db.Model):
    __tablename__ = 'auctions'
    auction_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)

class Bid(db.Model):
    __tablename__ = 'bids'
    bid_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    bidder_id = db.Column(db.Integer, db.ForeignKey('bidders.bidder_id'), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.auction_id'), nullable=False)

class Bidder(db.Model):
    __tablename__ = 'bidders'
    bidder_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BidHistory(db.Model):
    __tablename__ = 'bid_histories'
    history_id = db.Column(db.Integer, primary_key=True)
    bid_id = db.Column(db.Integer, db.ForeignKey('bids.bid_id'), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.auction_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    __tablename__ = 'reports'
    report_id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    generated_by = db.Column(db.Integer, db.ForeignKey('platform_owners.owner_id'), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    log_id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('platform_owners.owner_id'), nullable=False)


class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('bidders.bidder_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
