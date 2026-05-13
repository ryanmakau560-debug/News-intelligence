import tkinter as tk
from tkinter import messagebox, ttk
import database
# import scraper (uncomment this once you create scraper.py)

def handle_email_request():
    user = database.get_logged_in_user()
    if user:
        # If already logged in, show success
        email = user[0]
        messagebox.showinfo("Success", f"Intelligence report sent to {email}")
    else:
        # If not logged in, ask to authenticate
        response = messagebox.askyesno("Login Required", "You need to sign in with Google to email reports. Sign in now?")
        if response:
            # Here you would call your start_google_login function
            # For now, let's simulate a successful login:
            database.save_user("ryan@example.com", "Ryan")
            messagebox.showinfo("Auth Success", "Logged in! Click 'Email' again to send.")

# --- UI SETUP ---
root = tk.Tk()
root.title("News Intelligence System")
root.geometry("700x550")

# Main Container
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

tk.Label(main_frame, text="News Intelligence Dashboard", font=("Arial", 18, "bold")).pack(pady=10)

# The Notebook (Tabs) for Interactivity
notebook = ttk.Notebook(main_frame)
notebook.pack(fill="both", expand=True, pady=10)

# Tab 1: Live Feed
feed_tab = tk.Frame(notebook)
notebook.add(feed_tab, text=" Live Feed ")

feed_text = tk.Text(feed_tab, height=15)
feed_text.pack(fill="both", expand=True, padx=10, pady=10)
feed_text.insert("1.0", "Welcome! Click 'Fetch News' to start.")

# Tab 2: Watchlist
watch_tab = tk.Frame(notebook)
notebook.add(watch_tab, text=" My Watchlist ")
tk.Label(watch_tab, text="Add keywords to filter your news:").pack(pady=10)

# Tab 3: Bookmarks
book_tab = tk.Frame(notebook)
notebook.add(book_tab, text=" Bookmarks ")

# Control Buttons at the Bottom
btn_frame = tk.Frame(main_frame)
btn_frame.pack(fill="x", pady=10)

btn_scrape = tk.Button(btn_frame, text="Fetch Latest News", width=20)
btn_scrape.pack(side="left", padx=5)

btn_email = tk.Button(btn_frame, text="Email My Brief", bg="#4285F4", fg="white", 
                       width=20, font=("Arial", 10, "bold"), command=handle_email_request)
btn_email.pack(side="right", padx=5)

root.mainloop()