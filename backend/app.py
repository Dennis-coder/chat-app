from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

import jwt

import models.user as User
import models.friend as Friend
import models.group as Group
import models.message as Message
import models.group_message as GroupMessage
import models.report as Report

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
CORS(app)

@app.errorhandler(401)
def unauthorized(e):
    return jsonify(error=str(e)), 401

@auth.verify_token
def verify_token(token):
    try:
        payload = jwt.decode(token, "secret", algorithms="HS256")
        return payload
    except jwt.ExpiredSignatureError:
        abort(401, description='Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        abort(401, description='Invalid token. Please log in again.')

@auth.get_user_roles
def get_user_roles(user):
    return user["role"]


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
            "user": User.token(user)
        }

    return jsonify(response)

@app.post("/api/v1/user")
@auth.login_required
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
@auth.login_required(role=['user', 'admin'])
def update_user():
    user_id = auth.current_user()['id']
    pwd = request.json["password"]
    response = User.update_password(user_id, pwd)
    return response

@app.delete("/api/v1/user")
@auth.login_required(role=['user', 'admin'])
def delete_user():
    user_id = auth.current_user()['id']
    response = User.delete(user_id)
    return response

@app.get("/api/v1/user/find")
@auth.login_required(role=['user', 'admin'])
def find():
    user_id = auth.current_user()['id']
    term = request.args["term"]
    result = User.search(user_id, term)
    return jsonify(result)


@app.get("/api/v1/friend")
@auth.login_required(role=['user', 'admin'])
def get_friend():
    user_id = auth.current_user()['id']
    friend_id = request.args["friend_id"]
    friend = Friend.get(user_id, friend_id)
    return friend

@app.post("/api/v1/friend")
@auth.login_required(role=['user', 'admin'])
def post_friend():
    user_id = auth.current_user()['id']
    friend_id = request.json["friend_id"]
    result = Friend.add(user_id, friend_id)
    return result

@app.put("/api/v1/friend")
@auth.login_required(role=['user', 'admin'])
def put_friend():
    user_id = auth.current_user()['id']
    friend_id = request.json["friend_id"]
    result = Friend.accept(user_id, friend_id)
    return result

@app.delete("/api/v1/friend")
@auth.login_required(role=['user', 'admin'])
def delete_friend():
    user_id = auth.current_user()['id']
    friend_id = request.json["friend_id"]
    result = Friend.remove(user_id, friend_id)
    return result

@app.get("/api/v1/friend/all")
@auth.login_required(role=['user', 'admin'])
def all_friends():
    user_id = auth.current_user()['id']
    friends = Friend.get_all(user_id)
    return jsonify(friends)

@app.post("/api/v1/friend/message")
@auth.login_required(role=['user', 'admin'])
def message():
    text = request.json["text"]
    sender_id = auth.current_user()['id']
    reciever_id = request.json["reciever_id"]
    message = Message.new(text, sender_id, reciever_id)
    return message

@app.get("/api/v1/friend/messages")
@auth.login_required(role=['user', 'admin'])
def all_messages():
    user_id = auth.current_user()['id']
    friend_id = request.args["friend_id"]
    messages = Message.get_all(user_id, friend_id)
    return jsonify(messages)

@app.get("/api/v1/friend/requests")
@auth.login_required(role=['user', 'admin'])
def all_requests():
    user_id = auth.current_user()['id']
    requests = Friend.requests(user_id)
    return jsonify(requests)


@app.get("/api/v1/group")
@auth.login_required(role=['user', 'admin'])
def get_group():
    group_id = request.args["group_id"]
    group = Group.get(group_id)
    return group

@app.post("/api/v1/group")
@auth.login_required(role=['user', 'admin'])
def post_group():
    name = request.json["name"]
    owner = auth.current_user()['id']
    users = request.json["users"]
    group = Group.new(name, owner, users)
    return group

@app.put("/api/v1/group/name")
@auth.login_required(role=['user', 'admin'])
def put_group_name():
    group_id = request.json["group_id"]
    name = request.json["name"]
    group = Group.update_name(group_id, name)
    return group

@app.put("/api/v1/group/owner")
@auth.login_required(role=['user', 'admin'])
def put_group_owner():
    group_id = request.json["group_id"]
    owner = request.json["owner"]
    group = Group.update_owner(group_id, owner)
    return group

@app.delete("/api/v1/group")
@auth.login_required(role=['user', 'admin'])
def delete_group():
    group_id = request.json["group_id"]
    group = Group.delete(group_id)
    return group

@app.get("/api/v1/group/all")
@auth.login_required(role=['user', 'admin'])
def all_groups():
    user_id = auth.current_user()['id']
    groups = Group.get_all(user_id)
    return jsonify(groups)

@app.post("/api/v1/group/message")
@auth.login_required(role=['user', 'admin'])
def group_message():
    text = request.json["text"]
    sender_id = auth.current_user()['id']
    group_id = request.json["group_id"]
    message = GroupMessage.new(text, sender_id, group_id)
    return message

@app.get("/api/v1/group/messages")
@auth.login_required(role=['user', 'admin'])
def all_group_messages():
    group_id = request.args["group_id"]
    messages = GroupMessage.get_all(group_id)
    return jsonify(messages)

@app.post("/api/v1/group/member")
@auth.login_required(role=['user', 'admin'])
def post_member():
    group_id = request.json["group_id"]
    user_id = request.json["user_id"]
    result = Group.add_member(group_id, user_id)
    return result

@app.delete("/api/v1/group/member")
@auth.login_required(role=['user', 'admin'])
def delete_member():
    group_id = request.json["group_id"]
    user_id = request.json["user_id"]
    result = Group.remove_member(group_id, user_id)
    return result

@app.get("/api/v1/group/members")
@auth.login_required(role=['user', 'admin'])
def group_members():
    group_id = request.args["group_id"]
    members = Group.get_members(group_id)
    return jsonify(members)


@app.post("/api/v1/report")
@auth.login_required(role=['user', 'admin'])
def post_report():
    plaintiff_id = auth.current_user()['id']
    defendant = request.json["defendant"]
    reason = request.json["reason"]
    report = Report.new(plaintiff_id, defendant, reason)
    return jsonify(report)

@app.put("/api/v1/report")
@auth.login_required(role=['user', 'admin'])
def put_report():
    report_id = request.json["report_id"]
    status = request.json["status"]
    return Report.update_status(report_id, status)

@app.delete("/api/v1/report")
@auth.login_required(role=['user', 'admin'])
def delete_report():
    report_id = request.json["report_id"]
    return Report.delete(report_id)

@app.get("/test")
@auth.login_required(role=['user','admin'])
def test():
    return auth.current_user()