from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, HealthRecord, HealthRecordValue, HealthMetric

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main.route('/submit_record', methods=['GET', 'POST'])
@login_required
def submit_record():
    if request.method == 'POST':
        temperature = float(request.form['temperature'])
        blood_pressure_systolic = int(request.form['blood_pressure_systolic'])
        blood_pressure_diastolic = int(request.form['blood_pressure_diastolic'])
        heart_rate = int(request.form['heart_rate'])

        record = HealthRecord(user_id=current_user.id, temperature=temperature,
                              blood_pressure_systolic=blood_pressure_systolic,
                              blood_pressure_diastolic=blood_pressure_diastolic,
                              heart_rate=heart_rate)
        db.session.add(record)
        db.session.commit()
        flash('Health record added successfully', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('submit_record.html')

@main.route('/view_records')
@login_required
def view_records():
    records = HealthRecord.query.filter_by(user_id=current_user.id).all()
    return render_template('view_records.html', records=records)
