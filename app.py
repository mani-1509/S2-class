from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models.model_1 import db
from auth import auth_blueprint

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '5f4e4b8ed9731a35b54d401b9cfa32b3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize Extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Register Blueprints
app.register_blueprint(auth_blueprint)

# Home route
@app.route("/")
def home():
    return "Welcome to the app! Go to /login or /signup"

if __name__ == "__main__":
    app.run(debug=True)
