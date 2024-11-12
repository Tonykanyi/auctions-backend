from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction_platform.db'
    app.config['JWT_SECRET_KEY'] = 'vXkbGBTAbX'  # Replace with a secure key
    app.config['DEBUG'] = True  # Enable debug mode for development

    db.init_app(app)
    JWTManager(app)

    # Import and register blueprints from routes.py
    from .routes import auth_blueprint, user_blueprint, item_blueprint, auction_blueprint, bid_blueprint, notification_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(item_blueprint, url_prefix='/items')
    app.register_blueprint(auction_blueprint, url_prefix='/auctions')
    app.register_blueprint(bid_blueprint, url_prefix='/bids')
    app.register_blueprint(notification_blueprint, url_prefix='/notifications')

    return app
