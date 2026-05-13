import sqlite3

def init_db():
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()
    
    # 1. User Session (Stored after login)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_session (
            id INTEGER PRIMARY KEY,
            email TEXT,
            name TEXT
        )''')
    
    # 2. Scraped Articles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            category TEXT
        )''')

    # 3. Watchlist (User's Keywords) - NEW
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE
        )''')

    # 4. Bookmarks (Saved Articles) - NEW
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER,
            FOREIGN KEY (article_id) REFERENCES articles(id)
        )''')
        
    conn.commit()
    conn.close()

def save_user(email, name):
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_session") 
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