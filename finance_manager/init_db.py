import sqlite3

DATABASE = 'finance_manager.db'

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL
)
''')
conn.commit()
conn.close()

print("Database initialized.")
