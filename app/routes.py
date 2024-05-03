from flask import request, jsonify, abort
import logging
from functools import wraps
from .services import register_user, add_patient_measurement, authenticate_user
from .auth import authenticate, generate_token, required_token

logging.basicConfig(level=logging.INFO)

def configure_routes(app):

    def error_handler(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logging.error(f"An error occurred: {str(e)}")
                return jsonify({'error': 'An internal error occurred'}), 500
        return decorated_function

    @app.route('/')
    def index():
        return "Health Monitoring API is running!"

    @app.route('/users/register', methods=['POST'])
    @error_handler
    def handle_register_user():
        data = request.json
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        result, status_code = register_user(data)
        if status_code == 200:
            token = generate_token(data['email'])
            result.update({'token': token})
        return jsonify(result), status_code

    @app.route('/login', methods=['POST'])
    @error_handler
    def handle_login():
        data = request.json
        result, status_code = authenticate_user(data)
        if status_code == 200:
            token = generate_token(data['email'])
            result.update({'token': token})
        return jsonify(result), status_code

    @app.route('/patients/<int:patient_id>/measurements/add', methods=['POST'])
    @error_handler
    @required_token
    def handle_add_patient_measurement(patient_id):
        measurement = request.json
        result, status_code = add_patient_measurement(patient_id, measurement)
        return jsonify(result), status_code

    # Additional secure route 
    @app.route('/patients/<int:patient_id>', methods=['GET'])
    @error_handler
    @required_token
    def get_patient_details(patient_id):
        # Implementation to fetch patient details
        pass

# !!!keep implement the required_token decorator in auth module to check for valid tokens

