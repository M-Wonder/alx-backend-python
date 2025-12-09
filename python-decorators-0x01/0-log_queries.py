import sqlite3
import functools
from datetime import datetime

# decorator to log SQL queries
def log_queries(func):
    """Decorator that logs SQL queries before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query parameter
        # Check if 'query' is in kwargs first
        if 'query' in kwargs:
            query = kwargs['query']
        # Otherwise, assume it's the first positional argument
        elif args:
            query = args[0]
        else:
            query = None
        
        # Log the query with timestamp if found
        if query:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Executing query: {query}")
        
        # Execute the original function
        return func(*args, **kwargs)
    
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
