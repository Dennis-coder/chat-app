from models.db_handler import DBHandler
from models.helpers import parse_timestamp
import models.group as Group

def GroupMessageBean(params):
    return {
        "id": params[0],
        "text": params[1],
        "timestamp": parse_timestamp(params[2]),
        "senderId": params[3],
        "groupId": params[4]
    }


def get(id):
    with DBHandler() as db:
        db.execute("""
            SELECT *
            FROM group_messages 
            WHERE id = %s;
        """, [id])
        message = db.one()
    return GroupMessageBean(message)

def get_all(group_id):
    with DBHandler() as db:
        db.execute("""
            SELECT *
            FROM group_messages
            WHERE group_id = %s;
        """, [group_id])
        
        from_db = db.all()
    messages = []
    if from_db:
        for message in from_db:
            messages.append(GroupMessageBean(message))

    return messages

def new(text, sender_id, group_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO group_messages(text, timestamp, sender_id, group_id)
            VALUES(%s, 'now', %s, %s)
            RETURNING id;
        """, [text, sender_id, group_id])

        id = db.one()[0]
    Group.update_last_interaction(group_id)
    return get(id)
