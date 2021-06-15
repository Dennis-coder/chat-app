from flask import Flask, request, jsonify
from flask_cors import CORS
from models.auth import Auth

app = Flask(__name__)
auth = Auth()
CORS(app)


@app.errorhandler(401)
def unauthorized(e):
    return jsonify(error=str(e)), 401


@app.errorhandler(403)
def unauthorized(e):
    return jsonify(error=str(e)), 403


@app.get("/api/test")
@auth.login(roles=["user", "admin"])
def test():
    return auth.get_user() if auth.get_user() else "Hello"

import routes.user
import routes.friend
import routes.group
import routes.report