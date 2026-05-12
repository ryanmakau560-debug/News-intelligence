import sqlite3

def init_db():
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()
    # Table to store the Google account currently in use
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_session (
            id INTEGER PRIMARY KEY,
            email TEXT,
            name TEXT
        )
    ''')
    # Table for the news articles (Requirement: DB Usage)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            summary TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_user(email, name):
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_session") # Keep only one active user
    cursor.execute("INSERT INTO user_session (email, name) VALUES (?, ?)", (email, name))
    conn.commit()
    conn.close()

def get_logged_in_user():
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, name FROM user_session LIMIT 1")
    user = cursor.fetchone()
    conn.close()
    return user

init_db()