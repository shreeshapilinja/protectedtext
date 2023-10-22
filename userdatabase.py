import sqlite3 as s
import os
conn = s.connect('user_database.db')
cursor = conn.cursor()

# Create a 'users' table with 'username' as the primary key (unique and not null)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Commit the changes and close the database connection
conn.commit()
conn.close()

# Create the databases folder if it doesn't exist
os.makedirs('databases', exist_ok=True)

