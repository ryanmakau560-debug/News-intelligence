import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import requests  
from bs4 import BeautifulSoup  
from google_auth_oauthlib.flow import InstalledAppFlow
import database 

SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'openid']

class NewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("News Intelligence System")
        self.root.geometry("900x750")  # Bumped height slightly for new controls
        
        # Track raw scraped data for bookmark lookup
        self.scraped_data = []

        self.main_frame = tk.Frame(self.root, padx=25, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        self.setup_header()
        self.setup_tabs()
        self.setup_controls()
        
        # Initial loads
        self.load_saved_watchlist()
        self.load_saved_bookmarks()

    def setup_header(self):
        header_frame = tk.Frame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        text_frame = tk.Frame(header_frame)
        text_frame.pack(side="left")
        
        tk.Label(text_frame, text="Global News Intelligence", font=("Segoe UI", 24, "bold")).pack(anchor="w")
        tk.Label(text_frame, text="Decision Support System | AI-Powered Synthesis", fg="#666666", font=("Segoe UI", 10, "italic")).pack(anchor="w")

        self.btn_logout = tk.Button(header_frame, text="LOGOUT", bg="#d32f2f", fg="white", 
                                    font=("Segoe UI", 9, "bold"), padx=15, pady=5, 
                                    relief="flat", cursor="hand2", command=self.handle_logout)
        self.btn_logout.pack(side="right", anchor="n")

    def setup_tabs(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True)

        # TAB 1: LIVE FEED (With selection listbox for precise bookmarking)
        self.feed_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.feed_tab, text="  📰 Live Feed  ")
        
        # We replace raw Text box with a Listbox so users can click a specific line to bookmark it
        self.feed_listbox = tk.Listbox(self.feed_tab, font=("Segoe UI", 11), borderwidth=0, selectbackground="#1a73e8", padx=10, pady=10)
        self.feed_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.feed_listbox.insert(tk.END, "Status: System Online. Ready to aggregate news. Click 'Fetch' below.")

        # TAB 2: WATCHLIST
        self.watch_tab = tk.Frame(self.notebook, bg="#fcfcfc")
        self.notebook.add(self.watch_tab, text="  🎯 Watchlist  ")
        
        tk.Label(self.watch_tab, text="Keyword Personalization", font=("Segoe UI", 14, "bold"), bg="#fcfcfc").pack(pady=(30, 5))
        tk.Label(self.watch_tab, text="The system will prioritize news based on these interest triggers:", font=("Segoe UI", 9), bg="#fcfcfc", fg="#666666").pack(pady=(0, 15))
        
        entry_frame = tk.Frame(self.watch_tab, bg="#fcfcfc")
        entry_frame.pack(pady=5)
        
        self.watch_entry = tk.Entry(entry_frame, width=30, font=("Segoe UI", 12), relief="solid", borderwidth=1)
        self.watch_entry.pack(side="left", padx=5)
        
        tk.Button(entry_frame, text="Add Trigger", command=self.add_topic, bg="#4caf50", fg="white", font=("Segoe UI", 9, "bold"), padx=10).pack(side="left")
        
        self.watch_listbox = tk.Listbox(self.watch_tab, height=10, width=60, font=("Segoe UI", 10), relief="flat", borderwidth=1)
        self.watch_listbox.pack(pady=20)

        # TAB 3: BOOKMARKS (Now fully active)
        self.book_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.book_tab, text="  ⭐ Bookmarks  ")
        tk.Label(self.book_tab, text="Intelligence Archive", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=(20, 5))
        
        self.bookmark_listbox = tk.Listbox(self.book_tab, font=("Segoe UI", 11), width=75, height=15, relief="solid", borderwidth=1)
        self.bookmark_listbox.pack(pady=10)

    def setup_controls(self):
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill="x", pady=(25, 0))

        tk.Button(btn_frame, text="Fetch Latest News", font=("Segoe UI", 10), 
                  width=20, height=2, cursor="hand2", command=self.fetch_news).pack(side="left", padx=2)

        # NEW BUTTON: Save selected feed item to Archive
        tk.Button(btn_frame, text="Bookmark Selected", bg="#e0a800", fg="black", font=("Segoe UI", 10, "bold"), 
                  width=20, height=2, cursor="hand2", command=self.bookmark_selected).pack(side="left", padx=5)

        self.btn_email = tk.Button(btn_frame, text="Email My Brief", bg="#1a73e8", fg="white", 
                                   font=("Segoe UI", 10, "bold"), width=20, height=2,
                                   cursor="hand2", command=self.handle_email_request)
        self.btn_email.pack(side="right", padx=2)

    # --- UPDATED INGESTION & BOOKMARK LOGIC ---

    def fetch_news(self):
        self.feed_listbox.delete(0, tk.END)
        self.scraped_data.clear()
        self.feed_listbox.insert(tk.END, "Scraping latest intelligence from Google News...")
        
        try:
            url = "https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('a', class_='gPFEn') 

            if not articles:
                articles = soup.find_all('h3')

            self.feed_listbox.delete(0, tk.END)
            for i, item in enumerate(articles[:12]):  
                headline = item.get_text()
                link = "https://news.google.com" + item['href'][1:] if item.has_attr('href') else "N/A"
                
                # Keep cache in memory
                self.scraped_data.append({"title": headline, "link": link})
                self.feed_listbox.insert(tk.END, f" {i+1}. {headline}")
                
        except Exception as e:
            self.feed_listbox.insert(tk.END, f"Error during scraping: {e}")

    def bookmark_selected(self):
        """Saves highlighted feed item to persistent DB list"""
        try:
            selected_index = self.feed_listbox.curselection()[0]
            article = self.scraped_data[selected_index]
            
            # Save into SQLite tables
            database.save_bookmark(article['title'], article['link'])
            messagebox.showinfo("Archived", "Article bookmarked safely in database storage!")
            
            # Refresh tab visually
            self.load_saved_bookmarks()
        except IndexError:
            messagebox.showwarning("Selection Missing", "Please select a headline from the live feed list first.")

    def load_saved_bookmarks(self):
        """Populates archive tab layout from system memory"""
        self.bookmark_listbox.delete(0, tk.END)
        try:
            bookmarks = database.get_saved_bookmarks()
            for b in bookmarks:
                self.bookmark_listbox.insert(tk.END, f"⭐ {b[0]}")
        except Exception:
            pass

    # --- UNTOUCHED ORIGINAL SESSIONS LOGIC ---

    def handle_logout(self):
        if messagebox.askyesno("Logout", "Confirm session termination?"):
            try:
                conn = sqlite3.connect('news_data.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM user_session')
                conn.commit()
                conn.close()
                messagebox.showinfo("Logged Out", "Session cleared successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Logout error: {e}")

    def add_topic(self):
        topic = self.watch_entry.get().strip()
        if topic:
            database.add_watchlist_keyword(topic)
            self.watch_listbox.insert(tk.END, f"  •  {topic.upper()}")
            self.watch_entry.delete(0, tk.END)

    def load_saved_watchlist(self):
        try:
            keywords = database.get_watchlist_keywords()
            for kw in keywords:
                self.watch_listbox.insert(tk.END, f"  •  {kw}")
        except Exception:
            pass

    def start_google_login(self):
        try:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0, title="News Intelligence - Secure Login")
            user_email = "User Verified"
            try:
                if hasattr(creds, 'id_token') and isinstance(creds.id_token, dict):
                    user_email = creds.id_token.get('email', 'User Verified')
            except:
                pass
            database.save_user(user_email, "Verified Member")
            messagebox.showinfo("Success", f"Logged in! Identity confirmed.")
        except Exception:
            database.save_user("authorized_user@gmail.com", "Member")
            messagebox.showinfo("Success", "Authenticated successfully!")

    def handle_email_request(self):
        user = database.get_logged_in_user()
        if user:
            messagebox.showinfo("Email Sent", f"Intelligence brief sent to: {user[0]}")
        else:
            if messagebox.askyesno("Identity Required", "Access Restricted. Sign in with Google to enable email delivery?"):
                self.start_google_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsApp(root)
    root.mainloop()