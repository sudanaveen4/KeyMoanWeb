from flask import Flask, render_template, request, redirect, flash
import sqlite3
import re
import os
import json
import gspread
from datetime import datetime

app = Flask(__name__)
app.secret_key = "keymoan_final_key"

# --- LINKS ---
INSTALLER_ID = "1DD-CyW6fQg6T8Mk8kPAWHH1UoEHd975L"
THEME_LINKS = {
    'purple': "https://drive.google.com/uc?export=download&id=1d7nL0t3OwQV4s_PvUk_v0WM3i-aKEkZN",
    'blue':   "https://drive.google.com/uc?export=download&id=1d7nL0t3OwQV4s_PvUk_v0WM3i-aKEkZN",
    'orange': "https://drive.google.com/uc?export=download&id=1d7nL0t3OwQV4s_PvUk_v0WM3i-aKEkZN",
    'green':  "https://drive.google.com/uc?export=download&id=1d7nL0t3OwQV4s_PvUk_v0WM3i-aKEkZN"
}




# --- GOOGLE SHEETS CONNECTION ---
def save_to_sheet(fullname, email, mobile, insta):
    try:
        # Get the JSON key from Render Environment
        json_creds = os.environ.get("GOOGLE_SHEETS_JSON")
        
        if not json_creds:
            print("Error: No Google Credentials found in Environment!")
            return

        # Authenticate
        creds_dict = json.loads(json_creds)
        gc = gspread.service_account_from_dict(creds_dict)
        
        # Open the Sheet (Make sure name matches EXACTLY)
        sh = gc.open("KeyMoan_Data").sheet1
        
        # Add Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Append Row
        sh.append_row([fullname, email, mobile, insta, timestamp])
        print(f"Data saved to Google Sheet for {fullname}")
        
    except Exception as e:
        print(f"Google Sheet Error: {e}")

# --- SQLITE (Backup only) ---
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, fullname TEXT, email TEXT, mobile TEXT, insta TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html', t=THEME_LINKS)

@app.route('/submit', methods=['POST'])
def submit():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    insta = request.form.get('insta')

    # Validation
    if not all([fullname, email, mobile, insta]):
        flash("ERROR: All fields required.", "error")
        return redirect('/#download')

    if not re.match(r'^\d{10}$', mobile):
        flash("ERROR: Mobile must be 10 digits.", "error")
        return redirect('/#download')

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash("ERROR: Invalid Email.", "error")
        return redirect('/#download')

    # 1. Save to Google Sheet (Permanent)
    save_to_sheet(fullname, email, mobile, insta)

    # 2. Save to SQLite (Temporary Backup)
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (fullname, email, mobile, insta) VALUES (?, ?, ?, ?)",
                  (fullname, email, mobile, insta))
        conn.commit()
        conn.close()
    except:
        pass # Ignore SQLite errors if Google Sheet works

    return render_template('thankyou.html', download_link=INSTALLER_LINK)

# --- ADMIN PANEL (Optional View) ---
@app.route('/secret-leads')
def view_data():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        data = c.fetchall()
        conn.close()
        html = "<body style='background:#111;color:white;font-family:sans-serif'><h1>LOCAL BACKUP DATA</h1><table border='1'>"
        for row in data:
            html += f"<tr><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
        html += "</table></body>"
        return html
    except: return "No local data."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

def get_dl(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

