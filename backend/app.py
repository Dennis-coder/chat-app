from flask import Flask, request, jsonify

import models.user as User
import models.friend as Friend
import models.group as Group
import models.message as Message

app = Flask(__name__)

@app.route("/api/v1/user/register", methods=["POST"])
def register():
    user_data = request.get_json()
    user = User.register(**user_data)
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

@app.route("/api/v1/user/login", methods=["GET"])
def login():
    user_data = request.args
    user = User.login(**user_data)
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

@app.route("/api/v1/friend", methods=["GET", "POST", "PUT", "DELETE"])
def friend():
    if request.method == "GET":
        friend = Friend.get(**request.args)
        return friend

@app.route("/api/v1/friend/all", methods=["GET"])
def all_friends():
    friends = Friend.get_all(**request.args)
    return jsonify(friends)

@app.route("/api/v1/group/all", methods=["GET"])
def all_groups():
    groups = Group.get_all(**request.args)
    return jsonify(groups)

@app.route("/api/v1/message", methods=["POST"])
def message():
    if request.method == "POST":
        id = Message.new(**request.get_json())
        return Message.get(id)


@app.route("/api/v1/message/all", methods=["GET"])
def all_messages():
    messages = Message.get_all(**request.args)
    return jsonify(messages)