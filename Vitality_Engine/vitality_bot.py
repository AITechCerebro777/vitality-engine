import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
from datetime import datetime, timedelta

# --- 1. SETUP CREDENTIALS (FROM GITHUB SECRETS) ---
# We load the secrets from the Cloud Environment, not a local file.
TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE_NUMBER")
MY_PHONE = os.environ.get("MY_PHONE_NUMBER")

# Google Credentials (JSON string from Secret)
GCP_JSON = os.environ.get("GCP_SERVICE_ACCOUNT")

# --- 2. TIMEZONE MATH (CRITICAL) ---
# GitHub Servers live in UTC (London). We must force CST (Texas).
utc_now = datetime.utcnow()
cst_now = utc_now - timedelta(hours=6)
current_hour = cst_now.hour

print(f"🤖 VITALITY BOT ONLINE. Server Time (UTC): {utc_now.hour}:00")
print(f"📍 Adjusted Time (CST): {current_hour}:00")

# --- 3. THE BRAIN (DECISION LOGIC) ---
message_body = None

if current_hour == 5:
    message_body = "🌅 05:00 AM - IGNITION. The Architect is awake. Log your start."
elif current_hour == 13:
    message_body = "☕ 01:00 PM - CAFFEINE CUTOFF. Switch to water. Protect your sleep."
elif current_hour == 18:
    message_body = "⚔️ 06:00 PM - THE ARENA. Sweat Equity time. No excuses."
elif current_hour == 20:
    message_body = "🤐 08:00 PM - KITCHEN CLOSED. Fasting begins. Discipline equals Freedom."
else:
    print("⏳ No protocol event scheduled for this hour.")

# --- 4. EXECUTION (SEND SMS) ---
if message_body:
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE,
            to=MY_PHONE
        )
        print(f"✅ MESSAGE SENT: {message.sid}")
    except Exception as e:
        print(f"❌ ERROR: {e}")