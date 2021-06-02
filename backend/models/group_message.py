from models.db_handler import DBHandler
from models.helpers import parse_timestamp

def GroupMessage(params):
    return {
        "id": params["id"],
        "text": params['text'],
        "timestamp": parse_timestamp(params['timestamp']),
        "senderId": params['sender_id'],
        "groupId": params['group_id']
    }


def get(id):
    with DBHandler() as db:
        db.execute("""
            SELECT row_to_json(message_row)
            FROM (
                SELECT *
                FROM group_messages 
                WHERE id = %s
            ) AS message_row;
        """, [id])
        message = db.one()[0]
    return GroupMessage(message)

def get_all(group_id):
    with DBHandler() as db:
        db.execute("""
            SELECT json_agg(message_rows)
            FROM (
                SELECT *
                FROM group_messages
                WHERE group_id = %s
            ) AS message_rows
        """, [group_id])
        
        from_db = db.all()[0][0]
        messages = []
        if from_db:
            for message in from_db:
                messages.append(GroupMessage(message))

        return messages

def new(text, sender_id, group_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO group_messages(text, timestamp, sender_id, group_id)
            VALUES(%s, 'now', %s, %s)
            RETURNING id;
        """, [text, sender_id, group_id])

        id = db.one()[0]
        return id
