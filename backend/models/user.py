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
        user = db.one()[0]
        if user and bcrypt.checkpw(password.encode(), user['pwd_hash'].encode()):
            return User(user)
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

        return get(db.one()[0])


def token(user):
    return jwt.encode(user, "secret", algorithm="HS256")
