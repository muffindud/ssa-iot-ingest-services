from os import environ
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from routes.iot.auth import iot_auth_bp


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = environ.get('DEVICE_JWT_SECRET')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_VERIFY_SUB"] = False
jwt = JWTManager(app)

app.register_blueprint(iot_auth_bp, url_prefix='/iot/auth')
