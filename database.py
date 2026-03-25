import sqlite3

def create_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')

    conn.commit()
    conn.close()


def add_user(name, username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (name, username, password))
        conn.commit()
        return True
    except:
        return False


def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()

    return data