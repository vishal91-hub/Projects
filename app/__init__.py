from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from .commands import create_tables
import click
from flask.cli import with_appcontext
from flask import render_template
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
from app.models import User, AccountDetails 

app = Flask(__name__)
app.secret_key = 'ghtkk'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/sqlite/bank_app4.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
login_manager.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
with app.app_context(): # Create tables
     db.create_all()

from app import routes
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


