import getpass

from analyzer import security_report, show_recent
from auth import (create_user, find_user, is_strong, load_users, login,
                  save_users, verify_password, hash_password)
from logger import log_event

def show_banner():
    print("================================")
    print("   EMMA TECH IT MANAGEMENT")
    print("================================")

def get_new_password():
    while True:
        password = getpass.getpass("Set password: ")
        if not is_strong(password):
            print("Weak password. Use 8+ characters with upper case, "
                  "lower case and a number.")
            continue
        if password != getpass.getpass("Confirm password: "):
            print("Passwords do not match.")
            continue
        return password

def add_user(users, admin):
    username = input("New username: ").strip()
    role = input("Role (Admin / User): ").strip().capitalize()

    if username == "":
        print("Username cannot be empty.")
    elif find_user(users, username):
        print("That username already exists.")
    elif role not in ["Admin", "User"]:
        print("Role must be Admin or User.")
    else:
        create_user(users, username, get_new_password(), role)
        log_event("USER_CREATED", admin["username"],
                  f"created {username} as {role}")
        print("User created:", username)

def view_users(users):
    print("\nEMPLOYEES")
    for number, user in enumerate(users, start=1):
        status = "LOCKED" if user["locked"] else "Active"
        print(f"{number} - {user['username']} ({user['role']}) [{status}]")

def unlock_user(users, admin):
    username = input("Username to unlock: ").strip()
    target = find_user(users, username)
    if target is None:
        print("User not found.")
        return
    target["locked"] = False
    target["failed_attempts"] = 0
    save_users(users)
    log_event("ACCOUNT_UNLOCKED", admin["username"], f"unlocked {username}")
    print("Account unlocked:", username)

def change_password(users, user):
    current = getpass.getpass("Current password: ")
    if not verify_password(user, current):
        log_event("PASSWORD_CHANGE_FAILED", user["username"], "wrong current password")
        print("Current password is incorrect.")
        return
    new_password = get_new_password()
    user["salt"], user["hash"] = hash_password(new_password)
    save_users(users)
    log_event("PASSWORD_CHANGED", user["username"])
    print("Password changed.")

def admin_menu(user, users):
    while True:
        print("\nADMIN MENU")
        print("1. Add user")
        print("2. View users")
        print("3. Unlock account")
        print("4. View recent activity")
        print("5. Security report")
        print("6. Change my password")
        print("7. Logout")
        choice = input("Choose an option (1-7): ")

        if choice == "1":
            add_user(users, user)
        elif choice == "2":
            view_users(users)
        elif choice == "3":
            unlock_user(users, user)
        elif choice == "4":
            show_recent()
        elif choice == "5":
            security_report()
        elif choice == "6":
            change_password(users, user)
        elif choice == "7":
            break
        else:
            print("Invalid option.")

def user_menu(user, users):
    while True:
        print("\nUSER MENU")
        print("1. My profile")
        print("2. Change my password")
        print("3. Logout")
        choice = input("Choose an option (1-3): ")

        if choice == "1":
            print("Username:", user["username"])
            print("Role:", user["role"])
        elif choice == "2":
            change_password(users, user)
        elif choice == "3":
            break
        else:
            print("Invalid option.")

def main():
    users = load_users()
    show_banner()

    if not users:
        print("\nFirst-time setup: create the administrator account.")
        username = input("Admin username: ").strip()
        create_user(users, username, get_new_password(), "Admin")
        log_event("USER_CREATED", username, "first admin setup")

    while True:
        print("\n1. Login")
        print("2. Exit")
        choice = input("Choose an option (1-2): ")

        if choice == "1":
            user = login(users)
            if user:
                if user["role"] == "Admin":
                    admin_menu(user, users)
                else:
                    user_menu(user, users)
                log_event("LOGOUT", user["username"])
        elif choice == "2":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")

main()