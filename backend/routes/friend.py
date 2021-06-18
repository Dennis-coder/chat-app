from flask import request, jsonify
from app import app, auth
import models.friend as Friend
import models.message as Message


@app.get("/api/v1/friend")
@auth.login(roles=['user', 'admin'])
def get_friend():
    user_id = auth.user_id()
    friend_id = request.args["friend_id"]
    friend = Friend.get(user_id, friend_id)
    return friend


@app.post("/api/v1/friend")
@auth.login(roles=['user', 'admin'])
def post_friend():
    user_id = auth.user_id()
    friend_id = request.json["friend_id"]
    result = Friend.add(user_id, friend_id)
    return result


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


@app.get("/api/v1/friend/all")
@auth.login(roles=['user', 'admin'])
def all_friends():
    user_id = auth.user_id()
    friends = Friend.get_all(user_id)
    return jsonify(friends)


@app.post("/api/v1/friend/message")
@auth.login(roles=['user', 'admin'])
def message():
    text = request.json["text"]
    sender_id = auth.user_id()
    reciever_id = request.json["reciever_id"]
    message = Message.new(text, sender_id, reciever_id)
    return message


@app.get("/api/v1/friend/messages")
@auth.login(roles=['user', 'admin'])
def all_messages():
    user_id = auth.user_id()
    friend_id = request.args["friend_id"]
    messages = Message.get_all(user_id, friend_id)
    return jsonify(messages)


@app.get("/api/v1/friend/requests")
@auth.login(roles=['user', 'admin'])
def all_requests():
    user_id = auth.user_id()
    requests = Friend.requests(user_id)
    return jsonify(requests)
