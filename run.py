from flask import Flask

app = Flask(__name__)

from app.views import main, auth

app.register_blueprint(main)
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True)



