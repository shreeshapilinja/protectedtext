import sqlite3 as s
import os
conn = s.connect('user_database.db')
cursor = conn.cursor()

# Create a 'users' table with 'username' as the primary key and 'password' as an optional field
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY NOT NULL,
        password TEXT
    )
''')

# Commit the changes and close the database connection
conn.commit()
conn.close()

# Create the databases folder if it doesn't exist
os.makedirs('databases', exist_ok=True)

