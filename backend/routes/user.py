from flask import request, jsonify
from app import app, auth
import models.user as User

@app.post("/api/v1/user/login")
def login():
    username = request.json["username"]
    password = request.json["password"]
    user = User.login(username, password)
    if isinstance(user, str):
        response = {
            "status": "error",
            "error": user
        }

    else:
        response = {
            "status": "ok",
            "token": User.token(user)
        }

    return jsonify(response)


@app.post("/api/v1/user")
def register():
    username = request.json["username"]
    password = request.json["password"]
    user = User.register(username, password)
    if isinstance(user, str):
        response = {
            "status": "error",
            "error": user
        }

    else:
        response = {
            "status": "ok",
            "user": User.token(user)
        }

    return jsonify(response)


@app.put("/api/v1/user/password")
@auth.login(roles=['user', 'admin'])
def update_user():
    user_id = auth.user_id()
    pwd = request.json["password"]
    response = User.update_password(user_id, pwd)
    return response


@app.delete("/api/v1/user/self")
@auth.login(roles=['user', 'admin'])
def delete_user():
    user_id = auth.user_id()
    response = User.delete(user_id)
    return response

@app.delete("/api/v1/user")
@auth.login(roles=['admin'])
def delete_user_admin():
    user_id = request.json['user_id']
    response = User.delete(user_id)
    return response


@app.get("/api/v1/user/find")
@auth.login(roles=['user', 'admin'])
def find():
    user_id = auth.user_id()
    term = request.args["term"]
    result = User.search(user_id, term)
    return jsonify(result)
