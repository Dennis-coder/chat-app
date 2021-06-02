from models.db_handler import DBHandler
from models.helpers import parse_timestamp


def Friend(params):
    return {
        "id": params['id'],
        "username": params['username'],
        "lastInteraction": parse_timestamp(params["last_interaction"]),
        "friendsSince": parse_timestamp(params["friends_since"])
    }


def get_all(user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT json_agg(friend_rows)
            FROM (
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
                WHERE user_id = %s AND status = 0
            ) AS friend_rows
        """, [user_id, user_id])

        from_db = db.all()[0][0]
        friends = []
        if from_db:
            for friend in from_db:
                friends.append(Friend(friend))
        
        return friends

def get(user_id, friend_id):
    with DBHandler() as db:
        db.execute("""
            SELECT row_to_json(friend_row)
            FROM (
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
                WHERE user_id = %s AND user2_id = %s
            ) AS friend_row;
        """, [user_id, friend_id, user_id, friend_id])
        friend = db.one()[0]
    return Friend(friend)

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
            SELECT json_agg(user_rows)
            FROM (
                SELECT id, username, status, user_id AS sent_by
                FROM users
                LEFT JOIN friendships
                    ON (user_id = id AND user2_id = %s) OR (user_id = %s AND user2_id = id)
                WHERE status = 1
            ) AS user_rows;
        """, [user_id, user_id])

        requests = db.all()[0][0]

        return requests