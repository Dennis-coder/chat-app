import psycopg2
import traceback

conn = psycopg2.connect(database="websnap", host="127.0.0.1", port="5432")

class DBHandler:

    def __enter__(self):
        self.cur = conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.cur.close()
        if exc_type != None:
            traceback.print_exception(exc_type, exc_value, tb)
        else:
            conn.commit()


    def execute(self, query, values):
        if query[-1] != ";":
            query += ";"
        self.cur.execute(query, values)

    def one(self):
        return self.cur.fetchone()

    def all(self):
        return self.cur.fetchall()

