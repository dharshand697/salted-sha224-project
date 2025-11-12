# Simple dictionary attack simulator for demonstration only.
import sqlite3, hashlib, time

def load_wordlist(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return [w.strip() for w in f if w.strip()]

def crack_with_wordlist(stored_hash, salt_hex, wordlist):
    salt = bytes.fromhex(salt_hex)
    for w in wordlist:
        h = hashlib.sha224()
        h.update(salt + w.encode('utf-8'))
        if h.hexdigest() == stored_hash:
            return w
    return None

if __name__ == '__main__':
    db='database.db'
    wl='wordlist.txt'
    try:
        with open(wl,'r') as f: pass
    except FileNotFoundError:
        print('Create a small wordlist.txt with candidate passwords (one per line) to run this demo.')
        raise SystemExit(1)
    conn = sqlite3.connect(db)
    cur = conn.execute('SELECT username, salt, hash FROM users LIMIT 1')
    row = cur.fetchone()
    conn.close()
    if not row:
        print('No users in database. Register a user first.')
        raise SystemExit(1)
    username, salt_hex, stored_hash = row
    wordlist = load_wordlist(wl)
    start = time.time()
    found = crack_with_wordlist(stored_hash, salt_hex, wordlist)
    elapsed = time.time() - start
    if found:
        print(f'Cracked for user {username}:', found, f'in {elapsed:.3f}s')
    else:
        print('Password not found in wordlist. Time elapsed:', f'{elapsed:.3f}s')
