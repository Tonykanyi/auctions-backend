from flask import Blueprint, request, jsonify
from flask.views import MethodView
from ..models import Item
from .. import db

item_blueprint = Blueprint('item', __name__)

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
