from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction_platform.db'
    app.config['JWT_SECRET_KEY'] = 'vXkbGBTAbX'  # Replace with a secure key
    app.config['DEBUG'] = True  # Enable debug mode for development

    db.init_app(app)
    JWTManager(app)

    # Import and register blueprints
    from .routes.auth_routes import auth_blueprint
    from .routes.user_routes import user_blueprint
    from .routes.item_routes import item_blueprint
    from .routes.auction_routes import auction_blueprint
    from .routes.bid_routes import bid_blueprint
    from .routes.notification_routes import notification_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(item_blueprint, url_prefix='/items')
    app.register_blueprint(auction_blueprint, url_prefix='/auctions')
    app.register_blueprint(bid_blueprint, url_prefix='/bids')
    app.register_blueprint(notification_blueprint, url_prefix='/notifications')

    return app
