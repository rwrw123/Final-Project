from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health.db'
    app.config['SECRET_KEY'] = 'secretkey'

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Import models
        from . import models
        # Create all tables
        db.create_all()

    return app



