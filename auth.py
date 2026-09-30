import getpass
import hashlib
import json
import os
import secrets

from logger import log_event

USER_FILE = "users.json"
MAX_ATTEMPTS = 3

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), 200000
    )
    return salt, digest.hex()

def verify_password(user, password):
    _, attempt = hash_password(password, user["salt"])
    return secrets.compare_digest(attempt, user["hash"])

def is_strong(password):
    return (
        len(password) >= 8
        and any(c.isupper() for c in password)
        and any(c.islower() for c in password)
        and any(c.isdigit() for c in password)
    )

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return []

def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

def find_user(users, username):
    for user in users:
        if user["username"].lower() == username.lower():
            return user
    return None

def create_user(users, username, password, role):
    salt, pw_hash = hash_password(password)
    users.append({
        "username": username,
        "role": role,
        "salt": salt,
        "hash": pw_hash,
        "failed_attempts": 0,
        "locked": False,
    })
    save_users(users)

def login(users):
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    user = find_user(users, username)

    if user is None:
        log_event("LOGIN_FAILED", username, "unknown username")
        print("Invalid username or password.")
        return None

    if user["locked"]:
        log_event("LOGIN_BLOCKED", username, "account is locked")
        print("Account locked. Contact an administrator.")
        return None

    if verify_password(user, password):
        user["failed_attempts"] = 0
        save_users(users)
        log_event("LOGIN_SUCCESS", username, f"role={user['role']}")
        print(f"Welcome, {user['username']}.")
        return user

    user["failed_attempts"] += 1
    log_event("LOGIN_FAILED", username,
              f"attempt {user['failed_attempts']} of {MAX_ATTEMPTS}")
    if user["failed_attempts"] >= MAX_ATTEMPTS:
        user["locked"] = True
        log_event("ACCOUNT_LOCKED", username, "too many failed attempts")
        print("Too many failed attempts. Account locked.")
    else:
        print("Invalid username or password.")
    save_users(users)
    return None