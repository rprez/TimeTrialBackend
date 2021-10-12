from flask import Blueprint

auth_blueprint = Blueprint("session", __name__)

from app.auth import routes