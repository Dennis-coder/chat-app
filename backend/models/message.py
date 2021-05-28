from models.db_handler import DBHandler
from models.helpers import parse_timestamp

def Message(params):
    return {
        "id": params["id"],
        "text": params['text'],
        "timestamp": parse_timestamp(params['timestamp']),
        "senderId": params['sender_id'],
        "recieverId": params['reciever_id']
    }


def get(id):
    with DBHandler() as db:
        db.execute("""
            SELECT row_to_json(message_row)
            FROM (
                SELECT *
                FROM messages 
                WHERE id = %s
            ) AS message_row;
        """, [id])
        message = db.one()[0]
    return Message(message)

def get_all(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            SELECT json_agg(message_rows)
            FROM (
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
                )
            ) AS message_rows
        """, [user_id, friend_id, friend_id, user_id])
        
        from_db = db.all()[0][0]
        messages = []
        if from_db:
            for message in from_db:
                messages.append(Message(message))

        return messages

def new(text, sender_id, reciever_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO messages(text, timestamp, sender_id, reciever_id)
            VALUES(%s, 'now', %s, %s)
            RETURNING id;
        """, [text, sender_id, reciever_id])

        id = db.one()[0]
        print(id)
        return id
