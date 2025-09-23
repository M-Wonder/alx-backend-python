#!/usr/bin/env python3
"""
Seed script for MySQL database ALX_prodev.

This script:
- Connects to MySQL server
- Creates database ALX_prodev if not exists
- Creates user_data table if not exists
- Inserts data from user_data.csv
- Provides a generator to stream rows one by one
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid
from typing import Generator


def connect_db():
    """Connect to MySQL server (without selecting a database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword"  # <-- Replace with your MySQL root password
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except Error as e:
        print(f"Error while creating database: {e}")


def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",  # <-- Replace with your MySQL root password
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age DECIMAL NOT NULL
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error while creating table: {e}")


def insert_data(connection, csv_file):
    """Insert data from CSV file into the user_data table."""
    try:
        cursor = connection.cursor()
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = int(row["age"])
                try:
                    cursor.execute("""
                        INSERT IGNORE INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s);
                    """, (user_id, name, email, age))
                except Error as e:
                    print(f"Skipping row due to error: {e}")
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")


def stream_users(connection) -> Generator[tuple, None, None]:
    """
    Generator that streams rows from user_data table one by one.
    Yields (user_id, name, email, age).
    """
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")
    for row in cursor:
        yield row
    cursor.close()
