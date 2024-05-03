from flask import jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import mongo

ns = Namespace('admin', description='Admin operations')

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = mongo.db.users.find_one({'_id': user_id})
        if user and 'admin' in user['roles']:
            return fn(*args, **kwargs)
        else:
            return jsonify({"msg": "Admin access required"}), 403
    return wrapper

@ns.route('/secure-data')
class SecureData(Resource):
    @admin_required
    def get(self):
        return {"data": "Very sensitive data only for admins"}
