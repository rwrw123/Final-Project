from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from sqlalchemy.orm import Session
from . import db
from .models import HealthRecord, User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your dashboard.", "warning")
        return redirect(url_for('auth.login'))

    session_obj = Session(bind=db.engine)
    user = session_obj.get(User, user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    records = session_obj.query(HealthRecord).filter_by(user_id=user_id).all()
    session_obj.close()

    return render_template('dashboard.html', username=user.username, records=records)

@main.route('/submit_record', methods=['GET', 'POST'])
def submit_record():
    if 'user_id' not in session:
        flash("Please log in to submit a health record.", "warning")
        return redirect(url_for('auth.login'))

    session_obj = Session(bind=db.engine)
    user_id = session['user_id']
    if not session_obj.get(User, user_id):
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_record = HealthRecord(
            user_id=user_id,
            date=request.form['date'],
            temperature=request.form['temperature'],
            blood_pressure=request.form['blood_pressure'],
            heart_rate=request.form['heart_rate']
        )
        session_obj.add(new_record)
        session_obj.commit()
        session_obj.close()
        flash("Health record added successfully.", "success")
        return redirect(url_for('main.dashboard'))
    return render_template('submit_record.html')





