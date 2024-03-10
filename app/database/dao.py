import sqlite3 as sq

# Connect to database
db = sq.connect('app/database/main.db')
cur = db.cursor()

# ---------SELECT QUERIES----------

# -users-
async def get_users_all():
    return cur.execute('SELECT * FROM users').fetchall()

# -materials-
async def get_materials_all():
    return cur.execute('SELECT * FROM materials').fetchall()

async def get_material_by_name(m_name):
    return cur.execute('SELECT * FROM materials WHERE m_name = ?', (m_name,)).fetchone()

# -docs-
async def get_docs_all():
    return cur.execute('SELECT * FROM docs').fetchall()

async def get_docs_by_material(m_id):
    return cur.execute('SELECT * FROM docs WHERE m_id = ?', (m_id,)).fetchall()

async def get_doc_by_name(d_name):
    return cur.execute('SELECT * FROM docs WHERE d_name = ?', (d_name,)).fetchone()

# ---------INSERT QUERIES----------

# -users-
async def add_user(user_id, user_name):
    user = cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if not user:
        cur.execute('INSERT INTO users (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
        db.commit()
        
# -materials-
async def add_material(m_name):
    material = cur.execute('SELECT * FROM materials WHERE m_name = ?', (m_name,)).fetchone()
    if not material:
        cur.execute('INSERT INTO materials (m_name) VALUES (?)', (m_name,))
        db.commit()
        
# -docs-
async def add_doc(d_name, m_id, docs_id):
    cur.execute('INSERT INTO docs (d_name, m_id, docs_id) VALUES (?, ?, ?)', (d_name, m_id, docs_id))
    db.commit()


# ---------DELETE QUERIES----------

# -materials-
async def del_material(m_name):
    cur.execute('DELETE FROM materials WHERE m_name = ?', (m_name,))
    db.commit()
    
# -docs-
async def del_doc(d_name):
    cur.execute('DELETE FROM docs WHERE d_name = ?', (d_name,))
    db.commit()
    
async def del_docs_by_material(m_id):
    cur.execute('DELETE FROM docs WHERE m_id = ?', (m_id,))
    db.commit()

# ---------UPDATE QUERIES----------