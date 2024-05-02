from flask import Flask
from flask_restx import Api
from pymongo import MongoClient
from users import ns as users_ns
from devices import ns as devices_ns
from measurements import ns as measurements_ns

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017/")
db = client['health_db']

api.add_namespace(users_ns)
api.add_namespace(devices_ns)
api.add_namespace(measurements_ns)

if __name__ == '__main__':
    app.run(debug=True)
