from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from pymongo import MongoClient

# Setup MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['health_db']

ns = Namespace('auth', description='Authentication services')

# Model for user login
user_login_model = ns.model('Login', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password')
})

@ns.route('/login')
class UserLogin(Resource):
    @ns.expect(user_login_model)
    def post(self):
        """Authenticate user and return a JWT"""
        data = request.get_json()
        user = db.users.find_one({'email': data['email']})
        if user and check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify(access_token=access_token)
        else:
            return ns.abort(401, 'Invalid credentials')

def setup_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change to your real secret key
    jwt = JWTManager(app)
    return jwt
