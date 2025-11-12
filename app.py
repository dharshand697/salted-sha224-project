from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from utils import generate_salt, hash_password, verify_password
import os
RECAPTCHA_SITE_KEY = os.getenv("6Lc4YwosAAAAAEIf_UbRAlDM36xiIyv2w3w3SFTn")
ECAPTCHA_SECRET_KEY = os.getenv("6Lc4YwosAAAAAEIf_UbRAlDM36xiIyv2w3w3SFTn")

# ============================================================
#  CONFIGURATION
# ============================================================
DB = 'database.db'
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')  # Change for security

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Used for flash/session messages


# ============================================================
#  DATABASE INITIALIZATION
# ============================================================
def init_db():
    """Create the users table if it does not exist."""
    with sqlite3.connect(DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                salt BLOB,
                hash TEXT
            )
        ''')
        conn.commit()


# ============================================================
#  ROUTES
# ============================================================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


# ------------------ ADMIN DASHBOARD --------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Admin dashboard to view all users, salts, and hashes."""
    if request.method == 'POST':
        password = request.form['password']

        # Verify admin password
        if password != ADMIN_PASSWORD:
            flash('❌ Unauthorized access – invalid admin password', 'danger')
            return redirect(url_for('admin'))

        # Fetch all user data
        with sqlite3.connect(DB) as conn:
            cur = conn.execute('SELECT username, salt, hash FROM users ORDER BY username')
            users = cur.fetchall()

        return render_template('admin_dashboard.html', users=users)

    return render_template('admin_login.html')


# ------------------ USER REGISTRATION ------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user and store salted SHA-224 hash."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        # Validation
        if not username or not password:
            flash('⚠️ Username and password are required', 'danger')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('⚠️ Password must be at least 6 characters long', 'danger')
            return redirect(url_for('register'))

        # Generate salt and hash
        salt = generate_salt()
        hashed = hash_password(password, salt)

        try:
            with sqlite3.connect(DB) as conn:
                conn.execute(
                    'INSERT INTO users(username, salt, hash) VALUES (?, ?, ?)',
                    (username, salt.hex(), hashed)
                )
                conn.commit()

            flash('✅ Registration successful. You can now login.', 'success')
            return redirect(url_for('index'))

        except sqlite3.IntegrityError:
            flash('⚠️ Username already exists. Try another one.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')


# ------------------ USER LOGIN -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate user by verifying salted SHA-224 hash."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        # Check if both fields are filled
        if not username or not password:
            flash('⚠️ Please enter both username and password.', 'danger')
            return redirect(url_for('login'))

        # Check if user exists in database
        with sqlite3.connect(DB) as conn:
            cur = conn.execute('SELECT salt, hash FROM users WHERE username=?', (username,))
            row = cur.fetchone()

        # 🟡 If user not found → show a friendly message
        if not row:
            flash('❌ No account found for this username. Please register first.', 'warning')
            return redirect(url_for('register'))

        salt_hex, stored_hash = row
        salt = bytes.fromhex(salt_hex)

        # Verify password
        if verify_password(stored_hash, password, salt):
            session['user'] = username
            flash('✅ Login successful!', 'success')
            return render_template('result.html', username=username, success=True)
        else:
            flash('❌ Incorrect password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')



# ------------------ USER LOGOUT ------------------------------
@app.route('/logout')
def logout():
    """Logout the current user."""
    session.pop('user', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ============================================================
#  MAIN ENTRY POINT
# ============================================================
import os

if __name__ == '__main__':
    import os
    init_db()
    port = int(os.environ.get('PORT', 8080))  # Railway expects 8080
    print(f"🚀 Flask server running on port {port}")
    app.run(host='0.0.0.0', port=port)

