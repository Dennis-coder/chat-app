import jwt
import bcrypt

from models.db_handler import DBHandler
from models.friend import Friend


def User(params):
    return {
        "id": params['id'],
        "username": params['username'],
        "role": params['role']
    }


def get(id):
    with DBHandler() as db:
        db.execute("""
            SELECT row_to_json(user_row)
            FROM (
                SELECT id, username, role 
                FROM users 
                WHERE id = %s
            ) AS user_row;
        """, [id])
        user = db.one()[0]
    return User(user)

def login(username, password):
    with DBHandler() as db:
        db.execute("""
            SELECT row_to_json(user_row)
            FROM (
                SELECT *
                FROM users 
                WHERE username = %s
            ) AS user_row;
        """, [username])
        user = db.one()
    if user and bcrypt.checkpw(password.encode(), user[0]['pwd_hash'].encode()):
        return User(user[0])
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

def update(user_id, password = None, role = None):
    with DBHandler() as db:
        if password:
            db.execute("""
                UPDATE users
                SET pwd_hash = %s
                WHERE id = %s;
            """, [bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), user_id])
        if role:
            db.execute("""
                UPDATE users
                SET role = %s
                WHERE id = %s;
            """, [role, role])
    return "User has been updated"

def delete(user_id):
    with DBHandler() as db:
        db.execute("""
            DELETE FROM users
            WHERE id = %s;
        """, [user_id])
    return "User has been deleted"

def search(term, user_id):
    with DBHandler() as db:
        db.execute("""
            SELECT row_to_json(user_row)
            FROM (
                SELECT id, username, status, user_id AS sent_by
                FROM users 
                LEFT JOIN friendships
                    ON (user_id = id AND user2_id = %s) OR (user_id = %s AND user2_id = id)
                WHERE username ILIKE %s
            ) AS user_row;
        """, [user_id, user_id, term])

        perfect_match = db.one()

        db.execute("""
            SELECT json_agg(user_rows)
            FROM (
                SELECT id, username, status, user_id AS sent_by
                FROM users
                LEFT JOIN friendships
                    ON (user_id = id AND user2_id = %s) OR (user_id = %s AND user2_id = id)
                WHERE username NOT ILIKE %s 
                AND username ILIKE %s
            ) AS user_rows;
        """, [user_id, user_id, term, f"{term}%"])

        prefix_matches = db.all()[0][0]

        db.execute("""
            SELECT json_agg(user_rows)
            FROM (
                SELECT id, username, status, user_id AS sent_by
                FROM users
                LEFT JOIN friendships
                    ON (user_id = id AND user2_id = %s) OR (user_id = %s AND user2_id = id)
                WHERE username NOT ILIKE %s 
                AND username NOT ILIKE %s
                AND username ILIKE %s
            ) AS user_rows;
        """, [user_id, user_id, term, f"{term}%", f"%{term}%"])

        partial_matches = db.all()[0][0]
    
    users = [perfect_match[0]] if perfect_match else []
    users = users + prefix_matches if prefix_matches else users
    users = users + partial_matches if partial_matches else users

    return users


def token(user):
    return jwt.encode(user, "secret", algorithm="HS256")
