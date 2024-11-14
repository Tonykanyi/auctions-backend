from flask import Blueprint, request, jsonify
from flask.views import MethodView
from ..models import Auction
from .. import db
from ..utils import login_required  # Import from utils
from datetime import datetime

auction_blueprint = Blueprint('auction', __name__)

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
