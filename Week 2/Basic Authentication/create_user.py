import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("students.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

users = [
    ("admin", "admin123"),
    ("jyothi", "jyo123"),
    ("student", "student123")
]

for username, password in users:
    hashed_password = generate_password_hash(password)

    conn.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )

conn.commit()
conn.close()

print("Users created successfully")