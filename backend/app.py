from flask import Flask, request, jsonify

import models.user as User
import models.friend as Friend
import models.group as Group
import models.message as Message
import models.group_message as GroupMessage

app = Flask(__name__)

@app.route("/api/v1/user", methods=["GET", "POST", "PUT", "DELETE"])
def user():
    if request.method == "GET":
        return login()
    elif request.method == "POST":
        return register()
    elif request.method == "PUT":
        return update_user()
    elif request.method == "DELETE":
        return delete_user()

def register():
    user = User.register(**request.json)
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

def login():
    user = User.login(**request.args)
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

def update_user():
    response = User.update(**request.json)
    return response

def delete_user():
    response = User.delete(request.data.decode())
    return response

@app.route("/api/v1/user/find", methods=["GET"])
def find():
    result = User.search(**request.args)
    return jsonify(result)

@app.route("/api/v1/friend", methods=["GET", "POST", "PUT", "DELETE"])
def friend():
    if request.method == "GET":
        friend = Friend.get(**request.args)
        return friend
    elif request.method == "POST":
        result = Friend.add(**request.json)
        return result
    elif request.method == "PUT":
        result = Friend.accept(**request.json)
        return result
    elif request.method == "DELETE":
        result = Friend.remove(**request.json)
        return result

@app.route("/api/v1/friend/all", methods=["GET"])
def all_friends():
    friends = Friend.get_all(**request.args)
    return jsonify(friends)

@app.route("/api/v1/friend/message", methods=["POST"])
def message():
    if request.method == "POST":
        id = Message.new(**request.get_json())
        return Message.get(id)

@app.route("/api/v1/friend/messages", methods=["GET"])
def all_messages():
    messages = Message.get_all(**request.args)
    return jsonify(messages)

@app.route("/api/v1/friend/requests", methods=["GET"])
def all_requests():
    requests = Friend.requests(**request.args)
    return jsonify(requests)

@app.route("/api/v1/group", methods=["GET", "POST", "PUT", "DELETE"])
def group():
    if request.method == "GET":
        group = Group.get(**request.args)
        return group
    elif request.method == "POST":
        group = Group.add(**request.json)
        return group
    elif request.method == "PUT":
        group = Group.update(**request.json)
        return group
    elif request.method == "DELETE":
        group = Group.delete(**request.json)
        return group

@app.route("/api/v1/group/all", methods=["GET"])
def all_groups():
    groups = Group.get_all(**request.args)
    return jsonify(groups)

@app.route("/api/v1/group/message", methods=["POST"])
def group_message():
    if request.method == "POST":
        id = GroupMessage.new(**request.get_json())
        return GroupMessage.get(id)

@app.route("/api/v1/group/messages", methods=["GET"])
def all_group_messages():
    messages = GroupMessage.get_all(**request.args)
    return jsonify(messages)

@app.route("/api/v1/group/members", methods=["GET"])
def group_members():
    members = Group.get_members(**request.args)
    return jsonify(members)