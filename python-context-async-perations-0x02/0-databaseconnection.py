import sqlite3

# Class-based context manager for database connection
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        """Open database connection and return cursor"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection and handle exceptions"""
        if exc_type is not None:
            # If an exception occurred, rollback changes
            self.conn.rollback()
        else:
            # If no exception, commit changes
            self.conn.commit()
        
        # Always close the connection
        self.conn.close()
        
        # Return False to propagate exceptions (if any)
        return False


# Example usage with the context manager
if __name__ == "__main__":
    # Use the context manager to query the database
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
