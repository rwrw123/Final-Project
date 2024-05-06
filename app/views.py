from flask import Blueprint, render_template, request, redirect, url_for, session

main = Blueprint('main', __name__, template_folder='template')
auth = Blueprint('auth', __name__, template_folder='template')

# Dashboard route
@main.route('/')
def dashboard():
    if 'user_id' in session:
        records = get_records_for_user(session['user_id'])
        return render_template('dashboard.html', username="User", records=records)
    else:
        return redirect(url_for('auth.login'))

# Submit health record form route
@main.route('/submit-record-form')
def submit_record_form():
    if 'user_id' in session:
        return render_template('submit_record.html')
    else:
        return redirect(url_for('auth.login'))

# Submit health record route
@main.route('/submit-record', methods=['POST'])
def submit_record():
    if 'user_id' in session:
        save_record(session['user_id'], request.form)
        return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for('auth.login'))

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = authenticate_user(username, password)
        if user_id:
            session['user_id'] = user_id
            return redirect(url_for('main.dashboard'))
        else:
            return redirect(url_for('auth.login'))
    return render_template('login.html')

# Register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        create_user(username, password)
        return redirect(url_for('auth.login'))
    return render_template('register.html')

# Logout route
@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.dashboard'))





