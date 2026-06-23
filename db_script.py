import sqlite3, os
db_path = r'C:\Users\Diogo\.n8n\database.sqlite'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT id, name, type FROM credentials_entity WHERE type = "facebookGraphApi"')
    for r in cur.fetchall(): print('ID:', r[0], 'Name:', r[1])
    conn.close()
