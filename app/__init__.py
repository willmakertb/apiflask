import os


from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from .config import Config
from .auth import auth
from .models import UserModel
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS


login_manager = LoginManager()

login_manager.login_view = 'auth.login'






#@login_manager.user_loader
#def load_user(username):
#    return UserModel.query(username)


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(auth)

    #login_manager.init_app(app)


    return app
