from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)

    # Default configuration with a secret key for session management
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://new_username:new_password@localhost/your_database_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'v9C5OIo8V8Bf1PViyC3Dtw' 

    # Update configuration if specific config is provided
    if config:
        app.config.update(config)

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
