import gspread
from oauth2client.service_account import ServiceAccountCredentials

print("INITIATING VITALITY ENGINE...")

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# Ensure this matches your key file name exactly
creds = ServiceAccountCredentials.from_json_keyfile_name("vitality_key.json", scope)
client = gspread.authorize(creds)

# Ensure this matches your Google Sheet name exactly
sheet = client.open("Vitality_Engine_DB").worksheet("Daily_Logs")

print("CONNECTION SUCCESSFUL!")
sheet.update_acell('K2', 'SYSTEM ONLINE')
print("Write Successful: Checked cell K2.")