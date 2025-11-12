# Salted SHA-224 Demo (Flask)
Implementation of salted password hashing using SHA-224 with a simple Flask web demo.

## Features
- Register users: password is salted (16 bytes) and hashed with SHA-224.
- Login: verifies password by re-hashing with stored salt.
- Simple dictionary attack simulator (attack_simulation.py).
- Attractive minimal web UI with gradient design.

## How to run (Ubuntu / WSL / VirtualBox)
1. Install Python 3 and pip.
2. (Optional) Create a virtualenv:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Initialize database (optional - app will auto-init):
   ```
   python3 init_db.py
   ```
4. Run the Flask app:
   ```
   python3 app.py
   ```
5. Open browser at http://localhost:5000

## Attack demo
- Create `wordlist.txt` with candidate passwords (one per line).
- Run:
  ```
  python3 attack_simulation.py
  ```

## Notes
- This is an educational demo: SHA-224 is fast and not recommended for production password hashing. Use bcrypt/Argon2 in real systems.
