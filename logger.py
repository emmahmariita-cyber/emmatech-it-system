from datetime import datetime

LOG_FILE = "activity.log"

def log_event(event, username, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {event} | {username} | {details}\n"
    with open(LOG_FILE, "a") as file:
        file.write(line)