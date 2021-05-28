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
                WHERE user2_id = %s
                UNION
                SELECT user2_id AS id, username, last_interaction, friends_since
                FROM friendships
                LEFT JOIN users
                    ON user2_id = id
                WHERE user_id = %s
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