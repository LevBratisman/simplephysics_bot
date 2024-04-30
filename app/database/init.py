import sqlite3 as sq

# Connect to database
db = sq.connect('app/database/main.db')
cur = db.cursor()

# Create tables
async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id INTEGER, "
                "user_name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS materials("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "m_name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS docs("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "d_name TEXT, "
                "m_id INTEGER, "
                "docs_id TEXT, "
                "FOREIGN KEY (m_id) REFERENCES materials (id))")
    cur.execute("CREATE TABLE IF NOT EXISTS videos("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "v_name TEXT, "
                "v_id TEXT, "
                "v_caption TEXT)")
    db.commit()