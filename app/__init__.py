from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or "config.DevelopmentConfig")

    db.init_app(app)
    login.init_app(app)
    login.login_view = 'login'

    with app.app_context():
        from app import models, views
        db.create_all()

    return app








