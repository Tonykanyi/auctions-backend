from flask import Blueprint, request, jsonify
from flask.views import MethodView
from ..models import Bid
from .. import db
from ..utils import login_required  # Corrected to import from utils
from datetime import datetime

bid_blueprint = Blueprint('bid', __name__)

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
