#!/usr/bin/env python3
"""
Module: 0-stream_users
This module defines a generator that streams rows
from the user_data table one by one.
"""

import mysql.connector
from mysql.connector import Error
from typing import Generator, Dict


def stream_users() -> Generator[Dict[str, str], None, None]:
    """
    Generator that fetches rows from the user_data table one by one.
    Yields each row as a dictionary with keys:
    user_id, name, email, age
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",  # <-- replace with your MySQL root password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)  # rows as dicts
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:  # only ONE loop
            yield row
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Database error: {e}")
        return
