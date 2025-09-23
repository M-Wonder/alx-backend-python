#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields rows one by one, but fetches in batches"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # adjust username if needed
        password="root",   # adjust password if needed
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data;")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:          # <-- yield one row at a time
            yield row

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes rows streamed in batches,
    but filters users over age 25 only.
    """
    for user in stream_users_in_batches(batch_size):   # loop 1
        if user["age"] > 25:                          # filtering
            print(user)
    return
    
