import jwt
import datetime
from flask import request, jsonify
from functools import wraps
from .services import get_user_details  # Ensure this service exists and is implemented correctly

SECRET_KEY = "secret_key_here"

def generate_token(user_id, roles):
    """Generates a JWT token for authenticated users."""
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Token expires in one day
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
            'roles': roles
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
    except Exception as e:
        return str(e)

def decode_token(token):
    """Decodes the JWT token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return 'Token expired, please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token, please log in again.'

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = decode_token(token)
            current_user = get_user_details(data['sub'])  # Fetch the user details using the user ID in the token
        except Exception as e:
            return jsonify({'message': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 403
            try:
                data = decode_token(token)
                if not any(role in data['roles'] for role in allowed_roles):
                    return jsonify({'message': 'Permission denied'}), 403
            except Exception as e:
                return jsonify({'message': str(e)}), 401
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

