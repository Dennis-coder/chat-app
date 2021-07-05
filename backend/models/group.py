from models.db_handler import DBHandler
from models.helpers import parse_timestamp
from models.group_message import get_all as get_all_group_messages
import models.group_member as GroupMember


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


def get_with_messages(group_id):
    with DBHandler() as db:
        db.execute("""
            SELECT *
            FROM groups
            WHERE id = %s;
        """, [group_id])

        group = db.one()
    group = GroupBean(group)
    group['messages'] = get_all_group_messages(group['id'])
    group['members'] = GroupMember.get_all(group['id'])
    return group


def create(name, owner):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO groups(name, last_interaction, owner)
            VALUES(%s, 'now', %s)
            RETURNING id;
        """, [name, owner])

        id = db.one()[0]
    return id


def new(name, owner, users):
    group_id = create(name, owner)
    GroupMember.add(group_id, owner)
    for user in users:
        GroupMember.add(group_id, user)
    return get_with_messages(group_id)


def update_name(group_id, name):
    with DBHandler() as db:
        db.execute("""
            UPDATE groups
            SET name = %s
            WHERE id = %s;
        """, [name, group_id])
    return "Groupname has been updated"


def update_owner(group_id, owner):
    with DBHandler() as db:
        db.execute("""
            UPDATE groups
            SET owner = %s
            WHERE id = %s;
        """, [owner, group_id])
    return "Groupowner has been updated"


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


def get_all_with_messages(user_id):
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
            group = GroupBean(group)
            group['messages'] = get_all_group_messages(group['id'])
            group['members'] = GroupMember.get_all(group['id'])
            groups.append(group)

    return groups


def update_last_interaction(group_id):
    with DBHandler() as db:
        db.execute("""
            UPDATE groups
            SET last_interaction = 'now'
            WHERE id = %s;
        """, [group_id])
    return "Last interaction has been updated"


def is_member(group_id, user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT user_id
            FROM group_memberships
            WHERE group_id = %s
			AND user_id = %s;
        """, [group_id, user_id])
        user = db.one()
    return not not user