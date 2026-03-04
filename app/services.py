import secrets
import hashlib

def generate_api_key():
    key = secrets.token_urlsafe(32)
    return key

def hash_api_key(api_key: str):
    hashed = hashlib.sha256(api_key.encode()).hexdigest()
    return hashed