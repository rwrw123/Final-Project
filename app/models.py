from flask_pymongo import PyMongo
from app import mongo

def get_user_by_username(username):
    user = mongo.db.users.find_one({"username": username})
    if user:
        return user
    return None
