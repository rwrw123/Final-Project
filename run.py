from flask import Flask
from flask_restx import Api
from auth import setup_jwt, ns as auth_ns
from admin import ns as admin_ns

app = Flask(__name__)
api = Api(app)

# Initialize JWT
jwt = setup_jwt(app)

api.add_namespace(auth_ns)
api.add_namespace(admin_ns)

if __name__ == '__main__':
    app.run(debug=True)
