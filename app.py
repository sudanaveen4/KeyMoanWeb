from flask import Flask, render_template, request, redirect, flash
import sqlite3
import re

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

def get_dl(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

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

    if not all([fullname, email, mobile, insta]):
        flash("ERROR: All fields required.", "error")
        return redirect('/#download')

    if not re.match(r'^\d{10}$', mobile):
        flash("ERROR: Mobile must be 10 digits.", "error")
        return redirect('/#download')

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (fullname, email, mobile, insta) VALUES (?, ?, ?, ?)",
                  (fullname, email, mobile, insta))
        conn.commit()
        conn.close()
    except:
        flash("Database Error.", "error")
        return redirect('/#download')

    return render_template('thankyou.html', download_link=get_dl(INSTALLER_ID))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)