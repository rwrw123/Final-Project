from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime, timezone

# Initialize MongoDB 
mongo = PyMongo()

def register_user(data):
    if not data.get('email') or not data.get('name'):
        return {"error": "Missing name or email"}, 400
    if mongo.db.users.find_one({"email": data['email']}):
        return {"error": "User already exists"}, 409
    result = mongo.db.users.insert_one({
        "name": data['name'],
        "email": data['email'],
        "roles": data.get('roles', [])
    })
    return {"userId": str(result.inserted_id), "status": "success"}, 201

def add_patient_measurement(patient_id, measurement):
    result = mongo.db.measurements.insert_one({
        "patient_id": ObjectId(patient_id),
        "type": measurement['type'],
        "value": measurement['value'],
        "timestamp": datetime.now(timezone.utc)
    })
    return {"measurementId": str(result.inserted_id), "status": "success"}, 201

def delete_user(user_id):
    try:
        result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count:
            return {"status": "User deleted"}, 200
        else:
            return {"error": "User not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500