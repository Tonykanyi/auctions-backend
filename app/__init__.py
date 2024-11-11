from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction_platform.db'
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key
    app.config['DEBUG'] = True  # Enable debug mode for development

    db.init_app(app)
    JWTManager(app)

    # Register the routes blueprint
    from .routes import routes
    app.register_blueprint(routes, url_prefix='/api')

    return app
