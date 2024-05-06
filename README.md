# Final-Project
## Health monitoring system
  A health monitoring system designed with clean and simple interface for tracking health metrics like heart rate, blood pressure. The system features a backend support built with Flask. A frontend development utilizing HTML, JavaScript and CSS;facilitates with database using SQLite.

### Features
- User Authentication: Register, log in, and log out functionality.
- Dashboard: View health metrics and personalized greeting.
- Profile Management: Update personal information.
- Health Metrics: Submit and view health records.
- Responsive Design: Mobile and desktop-friendly layout.

### Installcation
- Python 3.9+
- Flask
- SQLite
  
### Setup
#### 1. Clone repository
     - git clone https://github.com/rwrw123/Final-Project
#### 2. Navigate to the project directory
#### 3. Create a virtual environment
     - python -m venv venv
#### 4. Activate virtual environment
##### On Windows
         - venv\Scripts\activate
##### On MacOS/Unix
         - source venv/bin/activate
#### 5. Install dependencies
       - pip install -r requirements.txt
#### 6. Set up the database
       - python setup_db.py

### Usage
#### 1. Start the Flask Server
        - python run.py
#### 2. Access the Application
        - Open browser and go http://127.0.0.1:5000

### Testing
#### Frontend 
- The frontend testing is using Jest
  ##### Run the test
          - npm start
#### Backend
- The backend testing is using unittest and Flask-Testing
  ##### Run the test
          - python -m unittest discover tests/py

   
