from models.db_handler import DBHandler, Transaction
from models.user import UserBean, get as get_user
from models.helpers import parse_timestamp


def GroupBean(params):
    return {
        "id": params[0],
        "name": params[1],
        "lastInteraction": parse_timestamp(params[2]),
        "owner": params[3]
    }


def get(group_id):
    with DBHandler() as db:
        db.execute("""
            SELECT *
            FROM groups
            WHERE id = %s;
        """, [group_id])

        group = db.one()
    return GroupBean(group)

def create(name, owner):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO groups(name, last_interaction, owner)
            VALUES(%s, 'now', %s)
            RETURNING id;
        """, [name, owner])

        id = db.one()[0]
    return get(id)

def new(name, owner, users):
    group = create(name, owner)
    add_member(group["id"], owner)
    for user in users:
        add_member(group["id"], user)
    return group

def update(group_id, name = None, owner = None):
    with DBHandler() as db:
        if name:
            db.execute("""
                UPDATE groups
                SET name = %s
                WHERE id = %s;
            """, [name, group_id])
        if owner:
            db.execute("""
                UPDATE groups
                SET owner = %s
                WHERE id = %s;
            """, [owner, group_id])
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
            SELECT id, name, last_interaction, owner
            FROM group_memberships
            LEFT JOIN groups
                ON group_id = id
            WHERE user_id = %s;
        """, [user_id])

        from_db = db.all()
    groups = []
    if from_db:
        for group in from_db:
            groups.append(GroupBean(group))
    
    return groups

def get_members(group_id):
    with DBHandler() as db:
        db.execute("""
            SELECT id, username, role
            FROM group_memberships
            LEFT JOIN users
                ON user_id = id
            WHERE group_id = %s;
        """, [group_id])

        from_db = db.all()
    members = []
    for member in from_db:
        members.append(UserBean(member))
    
    return members

def add_member(group_id, user_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO group_memberships(group_id, user_id, joined_at)
            VALUES(%s, %s, 'now');
        """, [group_id, user_id])
    return get_user(user_id)

def remove_member(group_id, user_id):
    with Transaction() as db:
        db.execute("""
            DELETE FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, [group_id, user_id])
        group = get(group_id)
        if group["owner"] == user_id:
            db.execute("""
                SELECT * 
                FROM group_memberships
                WHERE group_id = %s
            """, [group_id])
            id = db.one()[0]
            db.execute("""
                UPDATE groups
                SET owner = %s
                WHERE id = %s;
            """, [id, group_id])
    return "User removed from group"

def update_last_interaction(group_id):
    with DBHandler() as db:
        db.execute("""
            UPDATE groups
            SET last_interaction = 'now'
            WHERE id = %s;
        """, [group_id])
    return "Last interaction has been updated"