from os import environ
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from routes.user.access import user_access_bp


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = environ.get('USER_JWT_SECRET')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_VERIFY_SUB"] = False
jwt = JWTManager(app)

app.register_blueprint(user_access_bp, url_prefix='/user/access')
