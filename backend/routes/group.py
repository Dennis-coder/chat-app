from flask import request, jsonify
from app import app, auth
import models.group as Group
import models.group_message as GroupMessage
import models.group_member as GroupMember

@app.get("/api/v1/group")
@auth.login(roles=['user', 'admin'])
@auth.group_member
def get_group():
    group_id = request.args["group_id"]
    if 'includeMessages' in request.args and request.args['includeMessages'] == 'true':
        group = Group.get_with_messages(group_id)
    else:
        group = Group.get(group_id)
    return group


@app.post("/api/v1/group")
@auth.login(roles=['user', 'admin'])
def create_group():
    name = request.json["name"]
    owner = auth.user_id()
    users = request.json["users"]
    group = Group.new(name, owner, users)
    return group


@app.put("/api/v1/group/name")
@auth.login(roles=['user', 'admin'])
@auth.group_owner
def update_group_name():
    group_id = request.json["group_id"]
    name = request.json["name"]
    group = Group.update_name(group_id, name)
    return group


@app.put("/api/v1/group/owner")
@auth.login(roles=['user', 'admin'])
@auth.group_owner
def update_group_owner():
    group_id = request.json["group_id"]
    owner = request.json["owner"]
    group = Group.update_owner(group_id, owner)
    return group


@app.delete("/api/v1/group")
@auth.login(roles=['user', 'admin'])
@auth.group_owner
def delete_group():
    group_id = request.json["group_id"]
    group = Group.delete(group_id)
    return group


@app.get("/api/v1/groups")
@auth.login(roles=['user', 'admin'])
def all_groups():
    user_id = auth.user_id()
    if 'includeMessages' in request.args and request.args['includeMessages'] == 'true':
        groups = Group.get_all_with_messages(user_id)
    else:
        groups = Group.get_all(user_id)
    return jsonify(groups)


@app.post("/api/v1/group/message")
@auth.login(roles=['user', 'admin'])
@auth.group_member
def send_group_message():
    text = request.json["text"]
    sender_id = auth.user_id()
    group_id = request.json["group_id"]
    message = GroupMessage.new(text, sender_id, group_id)
    return message


@app.get("/api/v1/group/messages")
@auth.login(roles=['user', 'admin'])
@auth.group_member
def get_all_group_messages():
    group_id = request.args["group_id"]
    messages = GroupMessage.get_all(group_id)
    return jsonify(messages)


@app.post("/api/v1/group/member")
@auth.login(roles=['user', 'admin'])
@auth.group_owner
def add_member():
    group_id = request.json["group_id"]
    user_id = request.json["user_id"]
    result = GroupMember.add(group_id, user_id)
    return jsonify(result)


@app.delete("/api/v1/group/member")
@auth.login(roles=['user', 'admin'])
def delete_member():
    group_id = request.json["group_id"]
    user_id = request.json["user_id"]
    result = GroupMember.remove(group_id, user_id)
    return result


@app.get("/api/v1/group/members")
@auth.login(roles=['user', 'admin'])
@auth.group_member
def group_members():
    group_id = request.args["group_id"]
    members = GroupMember.get_all(group_id)
    return jsonify(members)
