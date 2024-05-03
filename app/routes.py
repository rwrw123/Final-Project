from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from .models import HealthRecord, User, db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('layout.html')

@main.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    user = User.query.get(user_id)
    records = HealthRecord.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', username=user.username, records=records)

@main.route('/submit_record', methods=['GET', 'POST'])
def submit_record():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        temperature = request.form['temperature']
        blood_pressure = request.form['blood_pressure']
        heart_rate = request.form['heart_rate']
        record = HealthRecord(user_id=user_id, date=date, temperature=temperature,
                              blood_pressure=blood_pressure, heart_rate=heart_rate)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('submit_record.html')

@main.route('/get_records', methods=['GET'])
def get_records():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    records = HealthRecord.query.filter_by(user_id=user_id).all()
    return jsonify([{'date': r.date.strftime('%Y-%m-%d'), 'temperature': r.temperature, 'blood_pressure': r.blood_pressure,
                     'heart_rate': r.heart_rate} for r in records]), 200
