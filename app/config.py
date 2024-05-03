import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/health_db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
