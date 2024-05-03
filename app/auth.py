import jwt
import datetime
from flask import request, jsonify
from config import Config
from database import mongo

def generate_refresh_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),  # Refresh token is long-lived
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256').decode('utf-8')
    save_refresh_token(user_id, token)
    return token

def save_refresh_token(user_id, token):
    mongo.db.refresh_tokens.update_one(
        {'user_id': user_id},
        {'$set': {'token': token, 'created_at': datetime.datetime.utcnow()}},
        upsert=True
    )


@app.route('/token/refresh', methods=['POST'])
def refresh_access_token():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Refresh token is required'}), 400

    payload = decode_token(refresh_token)
    if 'error' in payload:
        return jsonify({'error': payload['error']}), 401

    # Check if the token is stored in the database
    stored_token = mongo.db.refresh_tokens.find_one({'token': refresh_token})
    if not stored_token or stored_token['token'] != refresh_token:
        return jsonify({'error': 'Invalid refresh token'}), 401

    # Generate new access token
    user_id = payload['sub']
    new_access_token = generate_access_token(user_id, get_user_roles(user_id))
    return jsonify({'access_token': new_access_token})


def revoke_refresh_token(user_id):
    mongo.db.refresh_tokens.delete_one({'user_id': user_id})

def validate_refresh_token(token):
    payload = decode_token(token)
    if 'error' in payload:
        return False, payload['error']
    # Ensure the token exists in the database and is not revoked
    stored_token = mongo.db.refresh_tokens.find_one({'token': token})
    if not stored_token or stored_token['token'] != token:
        return False, 'Token revoked or does not exist'
    return True, None

def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        payload = decode_token(token)
        if 'error' in payload:
            return jsonify({'message': payload['error']}), 401
        return f(*args, **kwargs)
    return decorated

