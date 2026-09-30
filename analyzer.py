from collections import Counter

from logger import LOG_FILE

def read_log():
    try:
        with open(LOG_FILE, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def show_recent(count=20):
    lines = read_log()
    if not lines:
        print("No activity recorded yet.")
        return
    print(f"\nLAST {min(count, len(lines))} EVENTS")
    for line in lines[-count:]:
        print(line.strip())

def security_report():
    lines = read_log()
    if not lines:
        print("No activity recorded yet.")
        return

    failed = Counter()
    successes = 0
    locked = []

    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        timestamp, event, username = parts[0], parts[1], parts[2]

        if event == "LOGIN_FAILED":
            failed[username] += 1
        elif event == "LOGIN_SUCCESS":
            successes += 1
        elif event == "ACCOUNT_LOCKED":
            locked.append((timestamp, username))

    print("\nSECURITY REPORT")
    print("-" * 30)
    print("Successful logins:", successes)
    print("Failed logins:", sum(failed.values()))

    if failed:
        print("\nFailed attempts per account:")
        for username, count in failed.most_common():
            flag = "  <-- SUSPICIOUS" if count >= 3 else ""
            print(f"  {username}: {count}{flag}")

    if locked:
        print("\nAccounts locked:")
        for timestamp, username in locked:
            print(f"  {username} at {timestamp}")