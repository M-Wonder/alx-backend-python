import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # open connection
        self.conn = sqlite3.connect(self.db_name)
        print("[LOG] Database connection opened.")
        return self.conn  # this will be bound to the 'as' variable in with statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        # rollback if an exception occurred
        if exc_type is not None:
            self.conn.rollback()
            print(f"[ERROR] Exception occurred: {exc_val}. Rolled back transaction.")
        else:
            self.conn.commit()
            print("[LOG] Transaction committed.")
        
        # always close connection
        self.conn.close()
        print("[LOG] Database connection closed.")
        # return
