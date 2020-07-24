from flask import Flask
from flask_login import LoginManager

from movie_app.models import db, User

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from movie_app import views

