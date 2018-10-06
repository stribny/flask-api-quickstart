import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app_settings = os.getenv("APP_SETTINGS", "app.config.DevelopmentConfig")
app.config.from_object(app_settings)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.auth.views import auth_api

app.register_blueprint(auth_api, url_prefix="/api/v1/auth")

from app.auth.helpers import auth_required


@app.route("/ping")
def index():
    return jsonify({"status": "running"})


@app.route("/protected")
@auth_required
def protected():
    return jsonify({"message": "Protected message"})


from app.exceptions import AppError, NotFoundError


@app.errorhandler(404)
def custom404(error):
    return NotFoundError().to_api_response()


@app.errorhandler(Exception)
def handle_exception(exception):
    return AppError().to_api_response()


@app.errorhandler(AppError)
def handle_application_error(exception):
    return exception.to_api_response()
