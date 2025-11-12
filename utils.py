import hashlib, secrets

def generate_salt(size=16):
    return secrets.token_bytes(size)

def hash_password(password: str, salt: bytes) -> str:
    h = hashlib.sha224()
    # canonical: salt || password
    h.update(salt + password.encode('utf-8'))
    return h.hexdigest()

def verify_password(stored_hash: str, password: str, salt: bytes) -> bool:
    return stored_hash == hash_password(password, salt)
