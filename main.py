import tkinter as tk
from tkinter import messagebox
import database
from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Scope for requesting basic user info
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 
          'https://www.googleapis.com/auth/userinfo.profile', 'openid']

def start_google_login():
    try:
        # This looks for your Google Cloud credentials file
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Get user info from the credentials
        import requests
        response = requests.get(f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={creds.token}')
        user_info = response.json()
        
        email = user_info.get("email")
        name = user_info.get("name")
        
        # Save to Database
        database.save_user(email, name)
        messagebox.showinfo("Success", f"Welcome, {name}!\nLogged in with {email}")
        open_dashboard()
        
    except FileNotFoundError:
        messagebox.showerror("Setup Error", "client_secret.json not found. \n(See Google Cloud Console to download yours)")
    except Exception as e:
        messagebox.showerror("Login Error", f"Something went wrong: {e}")

def open_dashboard():
    login_frame.pack_forget() # Hide login
    dashboard_frame.pack(fill="both", expand=True)
    
    user = database.get_logged_in_user()
    if user:
        lbl_welcome.config(text=f"Logged in as: {user[0]}")

# UI Setup
root = tk.Tk()
root.title("News Intelligence System")
root.geometry("500x400")

# --- LOGIN FRAME ---
login_frame = tk.Frame(root)
login_frame.pack(pady=50)

tk.Label(login_frame, text="News Intelligence", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(login_frame, text="Use your Google account to receive daily briefs.").pack(pady=5)

btn_google = tk.Button(login_frame, text="Sign in with Google", command=start_google_login, 
                       bg="#4285F4", fg="white", font=("Arial", 11, "bold"), width=20, height=2)
btn_google.pack(pady=30)

# --- DASHBOARD FRAME (Hidden initially) ---
dashboard_frame = tk.Frame(root)

lbl_welcome = tk.Label(dashboard_frame, text="", font=("Arial", 10, "italic"))
lbl_welcome.pack(pady=10)

tk.Label(dashboard_frame, text="News Control Panel", font=("Arial", 16)).pack(pady=10)

# Placeholder for the next steps
btn_scrape = tk.Button(dashboard_frame, text="Fetch Latest News", width=25, bg="#eee")
btn_scrape.pack(pady=5)

btn_email = tk.Button(dashboard_frame, text="Email My Brief", width=25, bg="#eee")
btn_email.pack(pady=5)

root.mainloop()