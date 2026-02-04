import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONFIGURATION ---
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
KEY_FILE = "vitality_key.json"
SHEET_NAME = "Vitality_Engine_DB"
TAB_NAME = "Daily_Logs"

def connect_to_db():
    """Establishes connection to Google Sheets"""
    creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, SCOPE)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).worksheet(TAB_NAME)

def log_data(weight, calories, wake_time, notes):
    """Appends a new row of data to the database"""
    sheet = connect_to_db()
    
    # 1. Get Today's Date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 2. Prepare the Row (Order must match your Google Sheet Headers exactly!)
    # Headers: Date, Weight, Calories, Wake_Time, Meditation, Caffeine, Workout, Fasting, Sleep, Energy, Notes
    new_row = [
        today,          # A: Date
        weight,         # B: Weight
        calories,       # C: Calories
        wake_time,      # D: Wake Time
        False,          # E: Meditation (Checkbox - False means unchecked)
        True,           # F: Caffeine Cutoff (True means checked)
        True,           # G: Workout
        False,          # H: Fasting
        "21:30",        # I: Sleep Time
        8,              # J: Energy Level
        notes           # K: Notes
    ]
    
    # 3. Push to Cloud
    sheet.append_row(new_row)
    print(f"SUCCESS: Logged data for {today}")

# --- EXECUTION ---
print("Vitality Engine: Logging today's metrics...")
log_data(195.5, 1750, "05:30", "First automated log entry.")