import time
import sqlite3
import functools

# Decorator to open/close DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            print("[LOG] Database connection closed.")
    return wrapper


# Decorator to retry on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"[LOG] Attempt {attempt} of {retries}")
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
                    last_exception = e
                    print(f"[WARN] Database error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            # If all attempts fail, raise the last exception
            print("[ERROR] All retries failed.")
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(ret
