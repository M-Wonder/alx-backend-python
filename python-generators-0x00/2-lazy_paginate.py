#!/usr/bin/python3
import seed


def paginate_users(page_size, offset):
    """Fetch one page of users from DB with LIMIT/OFFSET."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator to lazily load user pages one by one.
    Only one loop is used, and yield is required.
    """
    offset = 0
    while True:  # single loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
    return
