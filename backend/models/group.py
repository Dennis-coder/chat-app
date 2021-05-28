from models.db_handler import DBHandler
from models.helpers import parse_timestamp


def Group(params):
    return {
        "id": params["id"],
        "name": params["name"],
        "lastInteraction": parse_timestamp(params["last_interaction"])
    }


def get_all(user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT json_agg(friend_rows)
            FROM (
                SELECT id, name, last_interaction, joined_at
                FROM group_memberships
                LEFT JOIN groups
                    ON group_id = id
                WHERE user_id = %s
            ) AS friend_rows
        """, [user_id])

        from_db = db.all()[0][0]
        groups = []
        if from_db:
            for group in from_db:
                groups.append(Group(group))
        
        return groups