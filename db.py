
import sqlite3

conn = sqlite3.connect("database.db")
print("Database opened successfully")

conn.execute("DROP TABLE IF EXISTS users")


conn.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")
print("Table 'users' created successfully")

conn.commit()

conn.close()
print("Database closed")
