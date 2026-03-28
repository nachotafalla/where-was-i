import sqlite3

def startdb():
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS library (id INTEGER PRIMARY KEY AUTOINCREMENT,
    tvmaze_id INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    image_url TEXT,
    status TEXT,
    premiered TEXT
    )
    """)
    conn.commit()
    conn.close()

def imagefb(image):
    if image:
        return image["medium"]
    else:
        return ""