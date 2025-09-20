import sqlite3

# Class-based context manager for database connection
class DatabaseConnection:
    def __init__(self, db_name="alx-airbnb-database
"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor  # return cursor for queries

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Error: {exc_val}, rolling back changes.")
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

# Example usage with the schema we made earlier
if __name__ == "__main__":
    # Fetch all users from Users table
    with DatabaseConnection("airbnb.db") as cursor:
        cursor.execute("SELECT id, name, email, age FROM Users")
        users = cursor.fetchall()
        print("[All Users]", users)

    # Fetch all properties
    with DatabaseConnection("airbnb.db") as cursor:
        cursor.execute("SELECT id, name, location, price FROM Properties")
        properties = cursor.fetchall()
        print("[All Properties]", properties)

    # Fetch bookings with user info
    with DatabaseConnection("airbnb.db") as cursor:
        cursor.execute("""
            SELECT b.id, u.name, p.name, b.start_date, b.end_date
            FROM Bookings b
            JOIN Users u ON b.user_id = u.id
            JOIN Properties p ON b.property_id = p.id
        """)
        bookings = cursor.fetchall()
        print("[Bookings with Users + Properties]", bookings)
