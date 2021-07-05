import jwt
import bcrypt
import datetime
from decouple import config

from models.db_handler import DBHandler
from models.friend_request import RequestBean


def UserBean(params):
    return {
        "id": params[0],
        "username": params[1],
        "role": params[2]
    }

def SearchResultBean(params):
    return {
        "id": params[0],
        "username": params[1]
    }


def get(id):
    with DBHandler() as db:
        db.execute("""
            SELECT id, username, role 
            FROM users 
            WHERE id = %s;
        """, [id])
        user = db.one()
    return UserBean(user)


def login(username, password):
    with DBHandler() as db:
        db.execute("""
            SELECT id, username, role, pwd_hash
            FROM users 
            WHERE username = %s;
        """, [username])
        user = db.one()
    if user and bcrypt.checkpw(password.encode(), user[3].encode()):
        return UserBean(user)
    else:
        return "Incorrect credentials"


def register(username, password):
    with DBHandler() as db:
        db.execute("""
            SELECT id 
            FROM users
            WHERE username = %s;
        """, [username])

        if db.one():
            return "Username has already been taken"

        db.execute("""
            INSERT INTO users(username, pwd_hash, role, created_at)
            VALUES(%s, %s, %s, 'now')
            RETURNING id;
        """, [username, bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), "user"])

        id = db.one()[0]
    return get(id)


def update_password(user_id, password=None):
    with DBHandler() as db:
        db.execute("""
            UPDATE users
            SET pwd_hash = %s
            WHERE id = %s;
        """, [bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), user_id])
    return "User has been updated"


def delete(user_id):
    with DBHandler() as db:
        db.execute("""
            DELETE FROM users
            WHERE id = %s;
        """, [user_id])
    return "User has been deleted"


def search(user_id, term):
    with DBHandler() as db:
        db.execute("""
            SELECT id, username
            FROM users 
            WHERE username ILIKE %s
            AND id != %s;
        """, [term, user_id])

        perfect_match = db.one()

        db.execute("""
            SELECT id, username
            FROM users 
            WHERE username NOT ILIKE %s 
            AND username ILIKE %s
            AND id != %s;
        """, [term, f"{term}%", user_id])

        prefix_matches = db.all()

        db.execute("""
            SELECT id, username
            FROM users 
            WHERE username NOT ILIKE %s 
            AND username NOT ILIKE %s
            AND username ILIKE %s
            AND id != %s;
        """, [term, f"{term}%", f"%{term}%", user_id])

        partial_matches = db.all()

    users = [SearchResultBean(perfect_match)] if perfect_match else []
    users = users + [SearchResultBean(x) for x in prefix_matches]
    users = users + [SearchResultBean(x) for x in partial_matches]

    return users


def token(user):
    payload = {
        **user,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=0, minutes=0, seconds=0),
    }

    return jwt.encode(payload, config('JWT_TOKEN_SECRET'), algorithm="HS256")
