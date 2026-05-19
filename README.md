# Comprehensive Setup & Guide: The News Intelligence Matrix v2.0

## What is this project?
The News Intelligence Matrix is a customized desktop dashboard program. It is designed to act as your own personal news station. Instead of opening a web browser and clicking through multiple news websites (like Reuters, AP, or BBC) that are full of slow-loading ads, pop-ups, and trackers, this app connects to those servers in the background. It instantly extracts the clean, raw text of the latest breaking headlines and organizes them all into one unified dark-mode screen.

Beyond just collecting text, it has a built-in Artificial Intelligence (AI) companion. When you click on a confusing or heavily detailed news story, you can send it to the AI box. The system automatically processes the article text and returns a simple, straightforward summary explaining why the story matters, who is involved, and what the historical background is. 

---

## How It Works Under the Hood (Simple Breakdown)

1. Ingestion Pipeline (The Scraper)
The application relies on Python's "BeautifulSoup4" package. Think of this like a digital vacuum cleaner. When you click a button in the user interface, this script sends a request to news feeds, ignores all images, videos, styling, and sidebars, and pulls back only the exact clean text characters of the news story. This makes updating your feed incredibly fast and saves internet bandwidth.

2. Neural Explainer Sandbox (The AI)
The raw news text is forwarded directly to the Google Gemini 2.5 Flash language model. Instead of relying on general-purpose AI chat screens, this connection acts as an isolated, strict analyst. It reads the article and breaks it down into structured sections like "Core Entities Involved" and "Geopolitical Impact," so you do not have to read through a massive wall of text to understand a complex global event.

3. Global Cloud Synchronization (The Database)
In older versions of this app, your data (like saved articles or tracked keywords) was written to a local database file sitting entirely on your computer's storage drive (SQLite3). This meant if you opened the app on a different machine, your saved data wouldn't be there. We have migrated this layer to MongoDB Atlas. Now, your keywords and bookmarks are transmitted as flexible, secure JSON data packages (called documents) directly to an online, serverless cloud database cluster. Everything stays synchronized no matter where you run the code.

4. User Interface Architecture (The Look)
The visual dashboard is generated using "CustomTkinter". This is a modern python toolkit that draws high-end user windows. It uses hardware acceleration (your computer's graphics card) to render a dark "Obsidian" or "Glassmorphic" layout, meaning the interface components look slightly translucent, smooth, and are designed specifically to look modern and reduce eye strain over hours of reading.

---

## The Complete Tech Stack Matrix

| Layer Name | Technology Used | What It Does In Your Project (Simple Terms) |
| :--- | :--- | :--- |
| Runtime Engine | Python 3.12 | The main brain framework that runs all code logic, text filtering, and software loops. |
| User Interface | CustomTkinter | The design engine that draws the actual desktop windows, tabs, dark-mode themes, and buttons. |
| Web Extractor | BeautifulSoup4 | The automation tool that connects to public news links and scrapes away the clean text. |
| Cloud Database | MongoDB Atlas | Your digital filing cabinet in the cloud that securely stores your custom search keywords and bookmarked items. |
| Intelligence API | Google Gemini 2.5 Flash | The neural processor that reads long news transcripts and instantly generates simple contextual summaries. |
| Identity Security | Google OAuth 2.0 | The login system that makes sure only verified operators can unlock and use the platform's advanced tools. |

---

## Step-by-Step Installation Guide for Beginners

Follow these steps precisely to get the entire intelligence matrix running locally on your computer.

### Step 1: Download the Project Code Files
You will need Git installed on your computer. Open your system terminal (or Git Bash / VS Code Terminal) and type the following commands to download your project folder from GitHub and move your terminal inside it:
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

### Step 2: Install the Python Package Libraries
Your core Python installation does not automatically know how to talk to MongoDB or run advanced dark-mode windows. You must install the external helper libraries. Run this exact pip command in your terminal:
pip install pymongo dnspython google-generativeai customtkinter beautifulsoup4

### Step 3: Set Up Your Private System Secrets
This app connects to your live MongoDB Cloud cluster and your personal Google Gemini AI account. To prevent your private secret passwords from being stolen or flagged by GitHub when you commit your code, you must inject them directly into your computer's system environment variables instead of typing them directly into your python files.

Open a **PowerShell** window on your computer and run these two lines, making sure to replace the placeholder text with your actual key strings:
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "YOUR_SECRET_GEMINI_KEY_STRING_HERE", "User")
[System.Environment]::SetEnvironmentVariable("MONGO_URI", "YOUR_LIVE_MONGODB_ATLAS_CONNECTION_STRING_HERE", "User")

*CRITICAL RESTART STEP:* After running those environment variable commands, you MUST completely close and reopen your VS Code editor or terminal window. If you do not restart it, your coding software will not be able to read the keys and your database connection will fail!

### Step 4: Run the Application
Now that your environment variables are locked in and your modules are installed, type this into your project terminal to launch your interface:
python main.py

---

## Navigating the Project Directory Structure

Here is a map of what every file inside your project folder does:

├── main.py              # The main control station. Running this script launches the GUI layout windows and controls what happens when buttons are clicked.
├── database.py          # The cloud delivery boy. This file contains the connection instructions that log into your MongoDB Atlas account and save/load documents.
├── client_secret.json   # Your secret Google login key file. It allows the software to pull down user validation scripts.
├── .gitignore           # The ultimate shield. A simple text file that tells Git exactly which secret files (like .json keys or old backup .db files) should NEVER be uploaded to the public internet.
└── README.md            # This exact text document—your software's manual guide.

---

## The Version History Roadmap

- [x] Version 1.0 (Local Build) — Initial app structure that saved data into a rigid, local file on your hard drive using SQLite3.
- [x] Version 1.5 (AI Connected) — Successfully created background threads to send news text blocks out to the Gemini AI API for summarization.
- [x] Version 2.0 (Cloud Migration) — Wiped out old local file storage completely and rebuilt the system to run on a globally synchronized MongoDB cloud cluster.
- [ ] Version 2.5 (Predictive Analysis) — Upcoming update that will count how many times target keywords are mentioned per day to forecast major trends before they happen.
- [ ] Version 3.0 (Cross-Platform compilation) — Upcoming update to pack this code into a standalone `.exe` or application file that works on mobile devices.

---

## Understanding the "Developer Sandbox" Fallback Mode

When you are testing or demonstrating this app, the Google login script (OAuth 2.0) will try to open up a web browser tab on your computer to verify your identity. Sometimes, your computer's built-in firewall rules or internet settings will block the app from receiving the browser's redirect signals (often resulting in a blank browser page or a "localhost connection closed" error).

To stop this connection issue from breaking your app or locking you out of your dashboard during presentations, the system has a built-in safety net called the **Developer Sandbox Fallback**.

If you hit a network issue, cancel out of the browser prompt, or if the connection port takes too long to respond, the backend code will print a safe alert to your console and automatically generate a mock operator profile:

- Simulated Profile Email: dev_sandbox_session@gmail.com
- Hardcoded Permission Path: SECURED // UNRESTRICTED_INTEL_2026

Once this fallback mode activates, it handles all interface security parameters internally. It completely bypasses the broken browser window and lets you go straight to your dashboard grids so you can scrape stories, use the Gemini Explainer box, and read from your live MongoDB cluster without any network interruption.
