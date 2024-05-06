from flask import Blueprint, render_template, request, redirect, url_for, session

main = Blueprint('main', __name__, template_folder='template')
auth = Blueprint('auth', __name__, template_folder='template')

users = {"test_user": "password123"}
user_records = {
    "test_user": [
        {"date": "2024-05-05", "temperature": 98.6, "blood_pressure": "120/80", "heart_rate": 72}
    ]
}

# Dashboard route
@main.route('/')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        username = get_username(user_id)
        records = get_records_for_user(user_id)
        return render_template('dashboard.html', username=username, records=records)
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
        user_id = session['user_id']
        record_data = {
            "date": request.form["date"],
            "temperature": float(request.form["temperature"]),
            "blood_pressure": request.form["blood_pressure"],
            "heart_rate": int(request.form["heart_rate"])
        }
        save_record(user_id, record_data)
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
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    return render_template('login.html')

# Register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success = create_user(username, password)
        if success:
            return redirect(url_for('auth.login'))
        else:
            error = "Registration failed"
            return render_template('register.html', error=error)
    return render_template('register.html')

# Logout route
@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.dashboard'))

# Helper functions

def get_records_for_user(user_id):
    return user_records.get(user_id, [])

def get_username(user_id):
    return user_id

def save_record(user_id, record_data):
    if user_id in user_records:
        user_records[user_id].append(record_data)
    else:
        user_records[user_id] = [record_data]

def authenticate_user(username, password):
    if username in users and users[username] == password:
        return username
    return None

def create_user(username, password):
    if username not in users:
        users[username] = password
        user_records[username] = []
        return True
    return False






