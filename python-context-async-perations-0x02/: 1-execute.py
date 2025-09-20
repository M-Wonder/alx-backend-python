import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # open connection and cursor
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        # execute query with parameters
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results   # makes results directly available in the 'with' block

    def __exit__(self, exc_type, exc_val, exc_tb):
        # rollback on error
        if exc_type:
            self.conn.rollback()
            print(f"[ERROR] Exception: {
