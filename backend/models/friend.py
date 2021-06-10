from models.db_handler import DBHandler
from models.helpers import parse_timestamp


def FriendBean(params):
    return {
        "id": params[0],
        "username": params[1],
        "lastInteraction": parse_timestamp(params[2]),
        "friendsSince": parse_timestamp(params[3])
    }

def RequestBean(params):
    return {
        "id": params[0],
        "username": params[1],
        "status": params[2],
        "sentBy": params[3]
    }


def get_all(user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT user_id AS id, username, last_interaction, friends_since
            FROM friendships
            LEFT JOIN users
                ON user_id = id
            WHERE user2_id = %s AND status = 0
            UNION
            SELECT user2_id AS id, username, last_interaction, friends_since
            FROM friendships
            LEFT JOIN users
                ON user2_id = id
            WHERE user_id = %s AND status = 0;
        """, [user_id, user_id])

        from_db = db.all()
    friends = []
    if from_db:
        for row in from_db:
            friends.append(FriendBean(row))
    
    return friends

def get(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            SELECT user_id AS id, username, last_interaction, friends_since
            FROM friendships
            LEFT JOIN users
                ON user_id = id
            WHERE user2_id = %s AND user_id = %s
            UNION
            SELECT user2_id AS id, username, last_interaction, friends_since
            FROM friendships
            LEFT JOIN users
                ON user2_id = id
            WHERE user_id = %s AND user2_id = %s;
        """, [user_id, friend_id, user_id, friend_id])
        friend = db.one()
    return FriendBean(friend)

def add(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO friendships (user_id, user2_id, status, last_interaction, friends_since)
            VALUES(%s, %s, 1, 'now', 'now');
        """, [user_id, friend_id])

        return "Sent friendsrequest"

def accept(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            UPDATE friendships
            SET status = 0
            WHERE (user_id, user2_id) = (%s, %s) OR (user_id, user2_id) = (%s, %s);
        """, [user_id, friend_id, friend_id, user_id])

    update_last_interaction(user_id, friend_id)
    return get(user_id, friend_id)

def remove(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            DELETE FROM friendships
            WHERE (user_id, user2_id) = (%s, %s) OR (user_id, user2_id) = (%s, %s);
        """, [user_id, friend_id, friend_id, user_id])

        return "Friend has been removed"

def requests(user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT id, username, status, user_id AS sent_by
            FROM users
            LEFT JOIN friendships
                ON (user_id = id AND user2_id = %s) OR (user_id = %s AND user2_id = id)
            WHERE status = 1;
        """, [user_id, user_id])

        from_db = db.all()
    requests = []
    if from_db:
        for row in from_db:
            requests.append(RequestBean(row))
    return requests

def update_last_interaction(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            UPDATE friendships
            SET last_interaction = 'now'
            WHERE (user_id = %s AND user2_id = %s) OR (user2_id = %s AND user_id = %s);
        """, [user_id, friend_id, user_id, friend_id])
    return "Last interaction has been updated"
