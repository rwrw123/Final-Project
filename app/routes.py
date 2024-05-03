from flask import Flask, request, jsonify, abort
from .services import (register_user, add_patient_measurement, delete_user, update_user, get_patient_details,
                       update_patient, delete_patient)
from .models import get_all_patients
from .auth import required_token, role_required

def configure_routes(app):

    @app.route('/')
    def index():
        return "Health Monitoring API is running!"

    @app.route('/users/register', methods=['POST'])
    @required_token
    @role_required(['Admin'])
    def handle_register_user():
        data = request.json
        result, status_code = register_user(data)
        return jsonify(result), status_code

    @app.route('/users/<user_id>/delete', methods=['DELETE'])
    @required_token
    @role_required(['Admin'])
    def handle_delete_user(user_id):
        result, status_code = delete_user(user_id)
        return jsonify(result), status_code

    @app.route('/users/<user_id>', methods=['PUT'])
    @required_token
    @role_required(['Admin'])
    def handle_update_user(user_id):
        data = request.json
        result, status_code = update_user(user_id, data)
        return jsonify(result), status_code

    @app.route('/patients', methods=['GET'])
    @required_token
    def handle_get_all_patients():
        patients = get_all_patients()
        return jsonify(patients), 200

    @app.route('/patients/<int:patient_id>', methods=['GET'])
    @required_token
    def handle_get_patient_details(patient_id):
        patient = get_patient_details(patient_id)
        if patient:
            return jsonify(patient), 200
        return jsonify({"error": "Patient not found"}), 404

    @app.route('/patients/<int:patient_id>', methods=['PUT'])
    @required_token
    def handle_update_patient(patient_id):
        data = request.json
        result, status_code = update_patient(patient_id, data)
        return jsonify(result), status_code

    @app.route('/patients/<int:patient_id>', methods=['DELETE'])
    @required_token
    def handle_delete_patient(patient_id):
        result, status_code = delete_patient(patient_id)
        return jsonify(result), status_code

    @app.route('/patients/<int:patient_id>/measurements/add', methods=['POST'])
    @required_token
    def handle_add_patient_measurement(patient_id):
        measurement = request.json
        result, status_code = add_patient_measurement(patient_id, measurement)
        return jsonify(result), status_code

if __name__ == '__main__':
    app = Flask(__name__)
    configure_routes(app)
    app.run(debug=True)


