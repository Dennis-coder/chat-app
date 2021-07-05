from models.db_handler import DBHandler, Transaction
from models.user import UserBean, get as get_user


def get_all(group_id):
    with DBHandler() as db:
        db.execute("""
            SELECT id, username, role
            FROM group_memberships
            LEFT JOIN users
                ON user_id = id
            WHERE group_id = %s
        """, [group_id])

        from_db = db.all()
    members = []
    for member in from_db:
        members.append(UserBean(member))

    return members


def add(group_id, user_id):
    with DBHandler() as db:
        db.execute("""
            INSERT INTO group_memberships(group_id, user_id, joined_at)
            VALUES(%s, %s, 'now');
        """, [group_id, user_id])
    return get_user(user_id)


def remove(group_id, user_id):
    with Transaction() as db:
        db.execute("""
            DELETE FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, [group_id, user_id])

        db.execute("""
            SELECT owner
            FROM groups
            WHERE id = %s;
        """, [group_id])

        if db.one() == user_id:
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
