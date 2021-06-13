from models.db_handler import DBHandler
from models.helpers import parse_timestamp
import models.friend as Friend

def MessageBean(params):
    return {
        "id": params[0],
        "text": params[1],
        "sent_at": parse_timestamp(params[2]),
        "senderId": params[3],
        "recieverId": params[4]
    }


def get(id):
    with DBHandler() as db:
        db.execute("""
            SELECT *
            FROM messages 
            WHERE id = %s;
        """, [id])
        message = db.one()
    return MessageBean(message)

def get_all(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            SELECT *
            FROM messages
            WHERE (
                sender_id = %s
                AND
                reciever_id = %s
            ) OR (
                sender_id = %s
                AND
                reciever_id = %s
            );
        """, [user_id, friend_id, friend_id, user_id])
        
        from_db = db.all()
    messages = []
    if from_db:
        for message in from_db:
            messages.append(MessageBean(message))

    return messages

def new(text, sender_id, reciever_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO messages(text, sent_at, sender_id, reciever_id)
            VALUES(%s, 'now', %s, %s)
            RETURNING id;
        """, [text, sender_id, reciever_id])

        id = db.one()[0]
    Friend.update_last_interaction(sender_id, reciever_id)
    return get(id)
