from flask import Blueprint, render_template, session, redirect, url_for, request
from sqlalchemy.orm import Session
from . import db
from .models import HealthRecord, User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    session_obj = Session(bind=db.engine)
    user = session_obj.get(User, session['user_id'])
    records = session_obj.query(HealthRecord).filter_by(user_id=user.id).all()
    session_obj.close()

    return render_template('dashboard.html', username=user.username, records=records)

@main.route('/submit_record', methods=['GET'])
def submit_record_form():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    return render_template('submit_record.html')

@main.route('/submit_record', methods=['POST'])
def submit_record():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    session_obj = Session(bind=db.engine)
    new_record = HealthRecord(
        user_id=session['user_id'],
        date=request.form['date'],
        temperature=request.form['temperature'],
        blood_pressure=request.form['blood_pressure'],
        heart_rate=request.form['heart_rate']
    )
    session_obj.add(new_record)
    session_obj.commit()
    session_obj.close()

    return redirect(url_for('main.dashboard'))




