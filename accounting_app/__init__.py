from flask import Flask
from flask_jwt_extended import *
from flask import jsonify, request, Response
from datetime import timedelta

import os

app = Flask(__name__)
app.config.from_pyfile("config.py", silent=True)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
# https://www.reddit.com/r/flask/comments/1hedkxa/flaskjwtextended_and_invalid_crypto_padding/
app.config["JWT_VERIFY_SUB"] = False

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({ "message": "The token has expired", "error": "token_expired" }), 401
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({ "message": "Signature verification failed", "error": "invalid_token" }), 401
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify({ "message": "Request does not contain an access token", "error": "authorization_required" }), 401
    )

import accounting_app.views
