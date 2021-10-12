from flask import Flask
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from datetime import timedelta

from app.auth import auth_blueprint
from app.users import users_blueprint

socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67dg3tg13g#'

    app.register_blueprint(auth_blueprint, url_prefix='/session')
    app.register_blueprint(users_blueprint, url_prefix='/users')

    jwt = JWTManager(app)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)  # = timedelta(minutes=15) !!!
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_HEADER_NAME"] = 'session_token'

    socketio.init_app(app,async_mode='eventlet')
    return app