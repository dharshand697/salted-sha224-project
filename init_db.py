import sqlite3
DB='database.db'
conn = sqlite3.connect(DB)
conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, salt BLOB, hash TEXT)')
conn.commit()
conn.close()
print('Database initialized at', DB)
