from flask import Blueprint, render_template, redirect, url_for, flash, request, session as session_obj
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager, bcrypt
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match", 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.password = password
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.dashboard'))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out', 'success')
    return redirect(url_for('main.home'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
