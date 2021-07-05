from models.db_handler import DBHandler
from models.helpers import parse_timestamp
from models.message import get_all as get_all_messages


def FriendBean(params):
    return {
        "id": params[0],
        "username": params[1],
        "lastInteraction": parse_timestamp(params[2]),
        "friendsSince": parse_timestamp(params[3])
    }


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

def get_with_messages(user_id, friend_id):
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
        friend_row = db.one()
    friend = FriendBean(friend_row)
    friend['messages'] = get_all_messages(user_id, friend_id)
    return friend

def add(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO friendships (user_id, user2_id, last_interaction, friends_since)
            VALUES(%s, %s, 'now', 'now');
        """, [user_id, friend_id])

    return "Friend added"

def remove(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            DELETE FROM friendships
            WHERE (user_id, user2_id) = (%s, %s) OR (user_id, user2_id) = (%s, %s);
        """, [user_id, friend_id, friend_id, user_id])

        return "Friend has been removed"

def get_all(user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT user_id AS id, username, last_interaction, friends_since
            FROM friendships
            LEFT JOIN users
                ON user_id = id
            WHERE user2_id = %s
            UNION
            SELECT user2_id AS id, username, last_interaction, friends_since
            FROM friendships
            LEFT JOIN users
                ON user2_id = id
            WHERE user_id = %s;
        """, [user_id, user_id])

        from_db = db.all()
    friends = []
    if from_db:
        for friend_row in from_db:
            friends.append(FriendBean(friend_row))
    
    return friends

def get_all_with_messages(user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT user_id AS id, username, last_interaction, friends_since
            FROM friendships
            LEFT JOIN users
                ON user_id = id
            WHERE user2_id = %s
            UNION
            SELECT user2_id AS id, username, last_interaction, friends_since
            FROM friendships
            LEFT JOIN users
                ON user2_id = id
            WHERE user_id = %s;
        """, [user_id, user_id])

        from_db = db.all()
    friends = []
    if from_db:
        for friend_row in from_db:
            friend = FriendBean(friend_row)
            friend['messages'] = get_all_messages(user_id, friend['id'])
            friends.append(friend)
    
    return friends

def update_last_interaction(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            UPDATE friendships
            SET last_interaction = 'now'
            WHERE (user_id = %s AND user2_id = %s) OR (user2_id = %s AND user_id = %s);
        """, [user_id, friend_id, user_id, friend_id])
    return "Last interaction has been updated"
