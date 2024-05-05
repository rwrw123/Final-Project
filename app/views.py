from flask import render_template, redirect, url_for, session, request, flash, Blueprint
from .models import db, User, HealthRecord
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    user = User.query.get(user_id)
    records = HealthRecord.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', username=user.username, records=records)

@main.route('/submit_record', methods=['GET', 'POST'])
@login_required
def submit_record():
    if request.method == 'POST':
        date = request.form.get('date')
        temperature = float(request.form.get('temperature'))
        blood_pressure = request.form.get('blood_pressure')
        heart_rate = int(request.form.get('heart_rate'))
        new_record = HealthRecord(
            user_id=current_user.id,
            date=date,
            temperature=temperature,
            blood_pressure=blood_pressure,
            heart_rate=heart_rate
        )
        db.session.add(new_record)
        db.session.commit()
        flash('Record submitted successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('submit_record.html')





