# Python Generators 0x00 - Database Seeder

This project sets up a MySQL database with a `user_data` table and streams rows using a generator.

## Requirements

- Ubuntu 18.04 LTS
- Python 3.7+
- MySQL server installed
- Install Python dependencies:
  ```bash
  pip install mysql-connector-python
Usage

Run the main script to create the database, table, and insert data:

./0-main.py


Expected output:

connection successful
Table user_data created successfully
Database ALX_prodev is present
[('uuid1', 'John Doe', 'john@example.com', 30), ('uuid2', 'Jane Smith', 'jane@example.com', 25)]

Streaming Users

You can also stream rows one by one with the generator:

import seed

conn = seed.connect_to_prodev()
for user in seed.stream_users(conn):
    print(user)
conn.close()


Output:

('uuid1', 'John Doe', 'john@example.com', 30)
('uuid2', 'Jane Smith', 'jane@example.com', 25)


---

✅ This setup includes:  
- Full **database setup** functions  
- **CSV seeding**  
- **Generator to stream rows**  

Do you want me to also write a **`0-main.py`** version that demonstrates streaming rows one by one using the `stream_users` generator?
