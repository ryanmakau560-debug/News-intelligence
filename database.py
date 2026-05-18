import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Database Core Matrix Connection String
# Hardcoded with your verified operational Atlas cluster details
MONGO_URI = os.environ.get("MONGO_URI") or "mongodb+srv://ryanmakau560_db_user:dXQg2faMLPkyxwIM@cluster0.4ged2lw.mongodb.net/news_intelligence_db?retryWrites=true&w=majority&appName=Cluster0"

try:
    # Initialize the secure cloud interface client
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Ping validation to confirm our cloud network passage is wide open
    client.admin.command('ping')
    db = client["news_intelligence_db"]
    
    # Establish dynamic document map spaces
    watchlist_col = db["watchlist"]
    bookmarks_col = db["bookmarks"]
    print("🤖 [DATABASE MATRIX] MongoDB Atlas Connection Successfully Established.")
except ConnectionFailure:
    print("⚠️ [DATABASE CRITICAL] Network passage timed out. Could not bind to MongoDB Atlas cluster.")
    db = None
    watchlist_col = None
    bookmarks_col = None


# --- WATCHLIST KEYPHRASE MANAGERS ---
def add_watchlist_keyword(keyword):
    """Inserts a clean, unique tracking keyword string directly into the cloud watchlist collection."""
    if watchlist_col is None:
        return
    clean_keyword = keyword.strip()
    if clean_keyword:
        # Uses update_one with an upsert flag to match case-insensitivity without duplicate conflicts
        watchlist_col.update_one(
            {"keyword": clean_keyword.lower()},
            {"$set": {"keyword": clean_keyword.lower(), "original_case": clean_keyword}},
            upsert=True
        )

def get_watchlist_keywords():
    """Retrieves all active keyword indicators currently logged across our cloud matrix."""
    if watchlist_col is None:
        return []
    try:
        cursor = watchlist_col.find({}, {"original_case": 1, "_id": 0})
        return [doc["original_case"] for doc in cursor]
    except Exception:
        return []


# --- ARCHIVE / BOOKMARK MANAGERS ---
def save_bookmark(title, link):
    """Saves a curated news title and direct source payload string to the cloud archive collection."""
    if bookmarks_col is None:
        return
    if title and link:
        # Prevent exact bookmark link replication using automated document indexing rules
        bookmarks_col.update_one(
            {"link": link},
            {"$set": {"title": title, "link": link}},
            upsert=True
        )

def get_saved_bookmarks():
    """Fetches all archived items structured into data sequences compatible with the UI map."""
    if bookmarks_col is None:
        return []
    try:
        cursor = bookmarks_col.find({}, {"title": 1, "link": 1, "_id": 0})
        # Outputs tuples (title, link) so main.py's list iteration b[0] stays completely intact
        return [(doc["title"], doc["link"]) for doc in cursor]
    except Exception:
        return []