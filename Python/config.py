#stores path 
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

#data tracking
from filelock import FileLock, Timeout
import csv
import getpass
from datetime import datetime

DOWNLOADS_FOLDER = Path.home() / "Downloads"
SETTINGS_FILE = Path(__file__).parent / "settings.json"


def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def get_folder(key, prompt_title):
    settings = load_settings()
    saved_path = settings.get(key)

    if saved_path and Path(saved_path).exists():
        return Path(saved_path)

    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Folder Setup", f"Please select your {prompt_title} folder.")
    chosen = filedialog.askdirectory(title=f"Select your {prompt_title} folder")

    root.destroy()

    if not chosen:
        messagebox.showerror("Setup Needed", f"No {prompt_title} folder was selected.")
        return None

    settings[key] = chosen
    save_settings(settings)
    return Path(chosen)

def change_folder(key, prompt_title):
    root = tk.Tk()
    root.withdraw()
    settings = load_settings()
    current_path = settings.get(key, "")

    start_dir = current_path if current_path and Path(current_path).exists() else str(Path.home())

    chosen = filedialog.askdirectory(title=f"Select your {prompt_title} folder", initialdir=start_dir)

    root.destroy()

    if not chosen:
        return None  # user cancelled, keep whatever was there before
    
    settings[key] = chosen
    save_settings(settings)
    return Path(chosen)

JHA_Folder = get_folder("JHA_Folder", "JHA - Autozone")
WO_Folder = get_folder("WO_Folder", "WO - Autozone")

LOGS_DIR = Path(__file__).parent.parent / "Logs"
LOGS_DIR.mkdir(exist_ok=True)  # creates the Logs folder if it doesn't already exist

USAGE_LOG_FILE = LOGS_DIR / "pdf_automation_usage_log.csv"
LOCK_FILE = str(USAGE_LOG_FILE) + ".lock"
USER_MAP_FILE = LOGS_DIR / "user_id_map.json"

def get_user_number():
    "Returns a persistent, anonymous 'usernumber' ID"
    username = getpass.getuser()

    if USER_MAP_FILE.exists():
        try: 
            with open(USER_MAP_FILE, "r") as f:
                mapping = json.load(f)
        except (json.JSONDecodeError, OSError):
            mapping ={}
    else:
        mapping = {}
    
    if username not in mapping:
        mapping[username] = f"User{len(mapping) + 1}"
        with open(USER_MAP_FILE, "w") as f:
            json.dump(mapping, f, indent=2)
    return mapping[username]

def log_usage(action, document_type=""):
    """
    Rewrites the usage log with updated totals at the top, followed by
    every individual event row (including this new one).
    action: "moved" or "deleted"
    document_type: "JHA" or "WO" (only relevant for "moved")
    """
    try:
        lock = FileLock(LOCK_FILE, timeout=5)
        with lock:
            user_id = get_user_number()
            timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")

            #Read exisiting individual rows
            rows = []
            if USAGE_LOG_FILE.exists():
                with open(USAGE_LOG_FILE, "r", newline ="") as f:
                    all_lines = list(csv.reader(f))
                if len(all_lines) > 7:
                    rows = all_lines[7: ]
            
            rows.append([timestamp, user_id, action.capitalize(), document_type])

            unique_users = set(row[1] for row in rows)
            total_moved = sum(1 for row in rows if row[2].lower() == "moved")
            total_jha = sum(1 for row in rows if row[2].lower() == "moved" and row[3] == "JHA")
            total_wo = sum(1 for row in rows if row[2].lower() == "moved" and row[3] == "WO")
            total_deleted = sum(1 for row in rows if row[2].lower() == "deleted")

            with open(USAGE_LOG_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Total Unique Users", len(unique_users)])
                writer.writerow(["Total Files Moved", total_moved])
                writer.writerow(["Total JHA Moved", total_jha])
                writer.writerow(["Total WO Moved", total_wo])
                writer.writerow(["Total Files Deleted", total_deleted])
                writer.writerow([])
                writer.writerow(["Timestamp", "User", "Action", "Document Type"])
                writer.writerows(rows)
    except Timeout:
        pass
    except Exception:
        pass

if __name__ == "__main__":
    print(f"LOGS_DIR = {LOGS_DIR}")
    print(f"LOGS_DIR exists? {LOGS_DIR.exists()}")
    log_usage("test", "JHA")
    print(f"USAGE_LOG_FILE exists after test? {USAGE_LOG_FILE.exists()}")