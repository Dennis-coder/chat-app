from flask import request, jsonify
from app import app, auth
import models.friend as Friend
import models.message as Message
import models.friend_request as FriendRequest


@app.get("/api/v1/friend")
@auth.login(roles=['user', 'admin'])
def get_friend():
    user_id = auth.user_id()
    friend_id = request.args["friend_id"]
    if 'includeMessages' in request.args and request.args['includeMessages'] == 'true':
        friend = Friend.get_with_messages(user_id, friend_id)
    else:
        friend = Friend.get(user_id, friend_id)
    return friend


@app.post("/api/v1/friend")
@auth.login(roles=['user', 'admin'])
def add_friend():
    user_id = auth.user_id()
    friend_id = request.json["friend_id"]
    result = Friend.add(user_id, friend_id)
    return jsonify(result)


@app.put("/api/v1/friend")
@auth.login(roles=['user', 'admin'])
def put_friend():
    user_id = auth.user_id()
    friend_id = request.json["friend_id"]
    result = Friend.accept(user_id, friend_id)
    return result


@app.delete("/api/v1/friend")
@auth.login(roles=['user', 'admin'])
def delete_friend():
    user_id = auth.user_id()
    friend_id = request.json["friend_id"]
    result = Friend.remove(user_id, friend_id)
    return result


@app.get("/api/v1/friends")
@auth.login(roles=['user', 'admin'])
def get_all_friends():
    user_id = auth.user_id()
    if 'includeMessages' in request.args and request.args['includeMessages'] == 'true':
        friends = Friend.get_all_with_messages(user_id)
    else:
        friends = Friend.get_all(user_id)
    return jsonify(friends)


@app.post("/api/v1/friend/message")
@auth.login(roles=['user', 'admin'])
def send_message():
    text = request.json["text"]
    sender_id = auth.user_id()
    reciever_id = request.json["reciever_id"]
    message = Message.new(text, sender_id, reciever_id)
    return message


@app.get("/api/v1/friend/messages")
@auth.login(roles=['user', 'admin'])
def get_all_messages():
    user_id = auth.user_id()
    friend_id = request.args["friend_id"]
    messages = Message.get_all(user_id, friend_id)
    return jsonify(messages)


@app.post("/api/v1/friend/request")
@auth.login(roles=['user', 'admin'])
def send_request():
    user_id = auth.user_id()
    friend_id = request.json["friend_id"]
    new_request = FriendRequest.send(user_id, friend_id)
    return jsonify(new_request)


@app.put("/api/v1/friend/request")
@auth.login(roles=['user', 'admin'])
def accept_request():
    user_id = auth.user_id()
    friend_id = request.json["friend_id"]
    new_request = FriendRequest.accept(user_id, friend_id)
    return jsonify(new_request)


@app.delete("/api/v1/friend/request")
@auth.login(roles=['user', 'admin'])
def delete_request():
    user_id = auth.user_id()
    friend_id = request.json["friend_id"]
    result = FriendRequest.delete(user_id, friend_id)
    return result


@app.get("/api/v1/friend/requests")
@auth.login(roles=['user', 'admin'])
def get_requests():
    user_id = auth.user_id()
    requests = FriendRequest.get_all(user_id)
    return jsonify(requests)


@app.get("/api/v1/friend/requests/pending")
@auth.login(roles=['user', 'admin'])
def get_pending_requests():
    user_id = auth.user_id()
    requests = FriendRequest.get_all_pending(user_id)
    return jsonify(requests)
