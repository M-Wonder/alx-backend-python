#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields rows in batches from user_data"""
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
        yield rows  # yield the whole batch at once

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over age 25
    and prints them one by one.
    """
    for batch in stream_users_in_batches(batch_size):   # loop 1
        for user in batch:                             # loop 2
            if user["age"] > 25:                       # filter condition
                print(user)
