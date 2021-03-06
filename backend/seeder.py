import psycopg2
import bcrypt


def seed():
    db = None
    try:
        db = connect()
        cur = db.cursor()
        drop_tables(cur)
        create_tables(cur)
        populate_tables(cur)
        cur.close()
        db.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()


def connect():
    return psycopg2.connect(database="db", host="127.0.0.1", port="5432", user="postgres", password="password")


def drop_tables(db):
    db.execute("DROP TABLE IF EXISTS users CASCADE;")
    db.execute("DROP TABLE IF EXISTS messages CASCADE;")
    db.execute("DROP TABLE IF EXISTS friendships CASCADE;")
    db.execute("DROP TABLE IF EXISTS groups CASCADE;")
    db.execute("DROP TABLE IF EXISTS group_memberships CASCADE;")
    db.execute("DROP TABLE IF EXISTS group_messages CASCADE;")
    db.execute("DROP TABLE IF EXISTS reports CASCADE;")
    db.execute("DROP TABLE IF EXISTS friend_requests CASCADE;")


def create_tables(db):
    db.execute("""
        CREATE TABLE users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(25) NOT NULL UNIQUE,
            pwd_hash VARCHAR NOT NULL,
            role VARCHAR(10) NOT NULL,
            created_at TIMESTAMP NOT NULL
        );
    """)
    db.execute("""
        CREATE TABLE messages(
            id SERIAL PRIMARY KEY,
            text VARCHAR(255) NOT NULL,
            sent_at TIMESTAMP NOT NULL,
            sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            reciever_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    db.execute("""
        CREATE TABLE friendships(
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            user2_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            last_interaction TIMESTAMP NOT NULL,
            friends_since TIMESTAMP NOT NULL,
            PRIMARY KEY (user_id, user2_id)
        );
    """)
    db.execute("""
        CREATE TABLE groups(
            id SERIAL PRIMARY KEY,
            name VARCHAR(25) NOT NULL,
            last_interaction TIMESTAMP NOT NULL,
            owner INTEGER NOT NULL REFERENCES users(id)
        );
    """)
    db.execute("""
        CREATE TABLE group_memberships(
            group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            joined_at TIMESTAMP NOT NULL
        );
    """)
    db.execute("""
        CREATE TABLE group_messages(
            id SERIAL PRIMARY KEY,
            text VARCHAR(255) NOT NULL,
            sent_at TIMESTAMP NOT NULL,
            sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE
        );
    """)
    db.execute("""
        CREATE TABLE reports(
            id SERIAL PRIMARY KEY,
            plaintiff_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            defendant_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            reason TEXT NOT NULL,
            status VARCHAR(10) NOT NULL,
            created_at TIMESTAMP NOT NULL
        );
    """)
    db.execute("""
        CREATE TABLE friend_requests(
            from_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            to_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            sent_at TIMESTAMP NOT NULL,
            PRIMARY KEY (from_id, to_id)
        );
    """)


def populate_tables(db):
    db.execute("INSERT INTO users (id, username, pwd_hash, role, created_at) VALUES(0, 'Deleted user', 'Deleted user', 'user', 'now');")

    password = b"asd"

    users = [
        {"username": "asd", "pwd_hash": bcrypt.hashpw(
            password, bcrypt.gensalt()), "role": "admin"},
        {"username": "asda", "pwd_hash": bcrypt.hashpw(
            password, bcrypt.gensalt()), "role": "user"},
        {"username": "asds", "pwd_hash": bcrypt.hashpw(
            password, bcrypt.gensalt()), "role": "user"},
        {"username": "asdd", "pwd_hash": bcrypt.hashpw(
            password, bcrypt.gensalt()), "role": "user"}
    ]

    for user in users:
        username = user["username"]
        pwd_hash = user["pwd_hash"].decode()
        role = user["role"]
        db.execute("""
            INSERT INTO users(username, pwd_hash, role, created_at) 
            VALUES(%s, %s, %s, 'now');
        """, [username, pwd_hash, role])

    messages = [
        {"text": "Message test 1", "sender_id": 1, "reciever_id": 2},
        {"text": "Message test 2", "sender_id": 2, "reciever_id": 1},
        {"text": "Message test 3", "sender_id": 1, "reciever_id": 3},
    ]

    for message in messages:
        text = message["text"]
        sender_id = message["sender_id"]
        reciever_id = message["reciever_id"]
        db.execute("""
            INSERT INTO messages(text, sent_at, sender_id, reciever_id) 
            VALUES (%s, 'now', %s, %s);
        """, [text, sender_id, reciever_id])

    friends = [
        {"user_id": 1, "user2_id": 2},
        {"user_id": 3, "user2_id": 1},
        {"user_id": 2, "user2_id": 4},
    ]

    for friend in friends:
        user_id = friend["user_id"]
        user2_id = friend["user2_id"]
        db.execute("""
            INSERT INTO friendships(user_id, user2_id, last_interaction, friends_since) 
            VALUES(%s, %s, 'now', 'now');
        """, [user_id, user2_id])

    groups = [
        {"name": "test group 1", "owner": 1},
        {"name": "test group 2", "owner": 2},
    ]

    for group in groups:
        name = group["name"]
        owner = group["owner"]
        db.execute("""
            INSERT INTO groups(name, last_interaction, owner) 
            VALUES(%s, 'now', %s);
        """, [name, owner])

    group_memberships = [
        {"group_id": 1, "user_id": 1},
        {"group_id": 1, "user_id": 2},
        {"group_id": 1, "user_id": 3},
        {"group_id": 2, "user_id": 2},
        {"group_id": 2, "user_id": 1},
        {"group_id": 2, "user_id": 4},
    ]

    for membership in group_memberships:
        group_id = membership["group_id"]
        user_id = membership["user_id"]
        db.execute("""
            INSERT INTO group_memberships(group_id, user_id, joined_at)
            VALUES(%s, %s, 'now')
        """, [group_id, user_id])

    group_messages = [
        {"text": "testerino", "sender_id": 1, "group_id": 1},
        {"text": "testerino", "sender_id": 2, "group_id": 1},
    ]

    for m in group_messages:
        text = m["text"]
        sender_id = m["sender_id"]
        group_id = m["group_id"]
        db.execute("""
            INSERT INTO group_messages(text, sent_at, sender_id, group_id)
            VALUES(%s, 'now', %s, %s)
        """, [text, sender_id, group_id])

    friend_requests = [
        {'from_id': 4, 'to_id': 1}
    ]

    for fr in friend_requests:
        from_id = fr['from_id']
        to_id = fr['to_id']
        db.execute("""
            INSERT INTO friend_requests(from_id, to_id, sent_at)
            VALUES(%s, %s, 'now')
        """, [from_id, to_id])


if __name__ == "__main__":
    seed()
