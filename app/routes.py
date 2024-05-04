from flask import Blueprint, render_template, session, redirect, url_for
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
        return redirect(url_for('auth.login'))

    session_obj = Session(bind=db.engine)
    user = session_obj.get(User, user_id)
    records = session_obj.query(HealthRecord).filter_by(user_id=user_id).all()
    session_obj.close()

    return render_template('dashboard.html', username=user.username, records=records)



