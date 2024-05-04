from flask import Blueprint, request, render_template, redirect, url_for, session,flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session_obj = Session(bind=db.engine)
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, password=password)
        session_obj.add(new_user)
        session_obj.commit()
        session_obj.close()
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session_obj = Session(bind=db.engine)
        username = request.form['username']
        password = request.form['password']
        user = session_obj.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session_obj.close()
            return redirect(url_for('main.dashboard'))
        session_obj.close()
        flash('Invalid credentials', 'Danger')
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Successfully logged out.', 'info')
    return redirect(url_for('main.home'))


