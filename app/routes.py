from flask import request, jsonify
from .services import register_user, add_patient_measurement

def configure_routes(app):

    @app.route('/')
    def index():
        return "Health Monitoring API is running!"

    @app.route('/users/register', methods=['POST'])
    def handle_register_user():
        data = request.json
        result, status_code = register_user(data)
        return jsonify(result), status_code

    @app.route('/patients/<int:patient_id>/measurements/add', methods=['POST'])
    def handle_add_patient_measurement(patient_id):
        measurement = request.json
        result, status_code = add_patient_measurement(patient_id, measurement)
        return jsonify(result), status_code

