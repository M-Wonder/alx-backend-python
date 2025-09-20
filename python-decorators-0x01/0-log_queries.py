import sqlite3
import functools

# decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # look for the 'query' argument (positional or keyword)
        query = None
        if "query" in kwargs:
            query = kwargs["query"]
        elif len(args) > 0:
            query = args[0]
        
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] Executing function without explicit query")
        
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

