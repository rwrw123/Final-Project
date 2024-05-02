from flask import Flask
from .routes import configure_routes
from .models import init_db

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/health_db"
    
    # Initialize MongoDB
    init_db(app)
    
    # Set up routes
    configure_routes(app)

    return app
