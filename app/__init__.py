import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.jwt_manager import jwt

db = SQLAlchemy()

def create_app():
    # Load configuration from .env file
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    jwt.init_app(app)

    from app.auth.routes import auth
    from app.recipe.routes import recipe_bp 

    app.register_blueprint(auth)
    app.register_blueprint(recipe_bp)

    # Create the database tables
    with app.app_context():
        db.create_all()

    return app
