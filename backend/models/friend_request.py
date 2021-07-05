from models.db_handler import DBHandler, Transaction
from models.friend import get_with_messages as get_friend


def RequestBean(params):
    return {
        "id": params[0],
        "username": params[1]
    }



def send(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO friend_requests(from_id, to_id, sent_at)
            VALUES(%s, %s, 'now');
        """, [user_id, friend_id])

    return "Sent friendsrequest"


def accept(user_id, friend_id):
    with Transaction() as db:
        db.execute("""
            DELETE FROM friend_requests
            WHERE from_id = %s 
            AND to_id = %s;
        """, [friend_id, user_id])

        db.execute("""
            INSERT INTO friendships (user_id, user2_id, last_interaction, friends_since)
            VALUES(%s, %s, 'now', 'now');
        """, [user_id, friend_id])

    return get_friend(user_id, friend_id)


def delete(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            DELETE FROM friend_requests
            WHERE (from_id = %s 
            AND to_id = %s)
            OR (from_id = %s
            AND to_id = %s);
        """, [friend_id, user_id, user_id, friend_id])
    return "Request deleted"


def get_all(user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT u.id, u.username
            FROM friend_requests AS fr
            LEFT JOIN users AS u
                ON from_id = u.id
            WHERE to_id = %s
        """, [user_id])

        from_db = db.all()
    requests = []
    if from_db:
        for row in from_db:
            requests.append(RequestBean(row))
    return requests


def get_all_pending(user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT u.id, u.username
            FROM friend_requests AS fr
            LEFT JOIN users AS u
                ON to_id = u.id
            WHERE from_id = %s
        """, [user_id])

        from_db = db.all()
    requests = []
    if from_db:
        for row in from_db:
            requests.append(RequestBean(row))
    return requests
