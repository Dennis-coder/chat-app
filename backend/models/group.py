from models.db_handler import DBHandler
from models.user import User
from models.helpers import parse_timestamp


def Group(params):
    return {
        "id": params["id"],
        "name": params["name"],
        "lastInteraction": parse_timestamp(params["last_interaction"]),
        "owner_id": params["owner_id"]
    }


def get(group_id):
    with DBHandler() as db:
        db.execute("""
            SELECT row_to_json(group_row)
            FROM (
                SELECT *
                FROM groups
                WHERE id = %s
            ) AS group_row
        """, [group_id])

        group = db.one()[0]
    return Group(group)

def add(name, user_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO groups(name, last_interaction, owner_id)
            VALUES(%s, 'now', %s)
            RETURNING id;
        """, [name, user_id])

        id = db.one()[0]
    return get(id)

def update(group_id, name = None, owner_id = None):
    with DBHandler() as db:
        if name:
            db.execute("""
                UPDATE groups
                SET name = %s
                WHERE id = %s;
            """, [name, group_id])
        if owner_id:
            db.execute("""
                UPDATE groups
                SET owner_id = %s
                WHERE id = %s;
            """, [owner_id, group_id])
    return "Group has been updated"

def delete(group_id):
    with DBHandler() as db:
        db.execute("""
            DELETE FROM groups
            WHERE id = %s;
        """, [group_id])

    return "Group has been deleted"

def get_all(user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT json_agg(friend_rows)
            FROM (
                SELECT id, name, last_interaction, owner_id
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

def get_members(group_id):
    with DBHandler() as db:
        db.execute("""
            SELECT json_agg(members)
            FROM (
                SELECT id, username, role
                FROM group_memberships
                LEFT JOIN users
                    ON user_id = id
                WHERE group_id = %s
            ) AS members
        """, [group_id])

        from_db = db.all()[0][0]
    members = []
    for member in from_db:
        members.append(User(member))
    
    return members