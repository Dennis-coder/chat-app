import psycopg2
import traceback
import time

def connect(tries = 0):
    try:
        return psycopg2.connect(database="db", host="database", port="5432", user="postgres", password="password")
    except:
        if tries == 0:
            return None
        time.sleep(0.5 * (5 / tries))
        return connect(tries - 1)

conn = connect()


class DBHandler:
    def __enter__(self):
        global conn
        if conn:
            self.cur = conn.cursor()
        else:
            conn = connect()
            if conn:
                self.cur = conn.cursor()
            else:
                raise Exception("Database connection could not be established")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.cur.close()
        if exc_type != None:
            traceback.print_exception(exc_type, exc_value, tb)
        else:
            conn.commit()

    def execute(self, query, values = [], tries = 0):
        query += ";"
        try:
            self.cur.execute(query, values)
        except Exception as err:
            if tries == 0:
                raise Exception("Database connection could not be established")
            time.sleep(0.5 * (5 / tries))
            self.execute(query, values, tries-1)

    def one(self):
        return self.cur.fetchone()

    def all(self):
        return self.cur.fetchall()

class Transaction():
    def __enter__(self):
        self.cur = conn.cursor()
        self.cur.execute("BEGIN;")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type != None:
            traceback.print_exception(exc_type, exc_value, tb)
            self.cur.execute("ROLLBACK;")
        else:
            self.cur.execute("COMMIT;")
            conn.commit()
        self.cur.close()

    def execute(self, query, values = []):
        query += ";"
        self.cur.execute(query, values)
    
    def one(self):
        return self.cur.fetchone()

    def all(self):
        return self.cur.fetchall()
