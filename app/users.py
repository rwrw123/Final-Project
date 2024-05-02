from flask import request
from flask_restx import Resource, Namespace, fields, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

# Setup MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['health_db']

# Namespace definition
ns = Namespace('users', description='User operations')

# Model definition
user_model = ns.model('User', {
    'name': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password')
})

# User Resource
@ns.route('/')
class UserList(Resource):
    @ns.marshal_list_with(user_model, envelope='data')
    def get(self):
        """List all users"""
        users = db.users.find()
        return list(users)

    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = ns.payload
        data['password'] = generate_password_hash(data['password'])
        db.users.insert_one(data)
        return data, 201

# Single User Resource
@ns.route('/<string:id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The user identifier')
class User(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, id):
        """Fetch a specific user"""
        user = db.users.find_one({'_id': id})
        if not user:
            ns.abort(404, "User not found")
        return user

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, id):
        """Delete a specific user"""
        db.users.delete_one({'_id': id})
        return '', 204

    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, id):
        """Update a specific user"""
        data = ns.payload
        db.users.update_one({'_id': id}, {"$set": data})
        return data
