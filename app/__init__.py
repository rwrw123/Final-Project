from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/health_db'
    else:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create sql tables for data models

    from .routes import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    return app
