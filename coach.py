import time
import schedule
import streamlit as st
from twilio.rest import Client
from datetime import datetime

# --- CONFIGURATION ---
account_sid = st.secrets["twilio"]["account_sid"]
auth_token = st.secrets["twilio"]["auth_token"]
from_number = st.secrets["twilio"]["from_number"]
to_number = st.secrets["twilio"]["to_number"]

client = Client(account_sid, auth_token)

# --- THE COUNTDOWN ENGINE ---
def get_mission_status():
    """Calculates days remaining until the SBMT Conference."""
    target_date = datetime(2026, 4, 16)
    current_date = datetime.now()
    delta = target_date - current_date
    days_left = delta.days
    return days_left

# --- THE TRANSMITTER ---
def send_vitality_signal(message_body):
    try:
        print(f"⚡ [FIRING] Sending signal: {message_body}")
        client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"✅ [SENT] Signal Delivered.")
    except Exception as e:
        print(f"❌ [ERROR] {e}")

# --- THE ROUTINES (UPGRADED) ---

def routine_ignition():
    days = get_mission_status()
    msg = (
        f"🌅 05:00 AM | THE IGNITION\n\n"
        f"⏰ T-MINUS {days} DAYS to SBMT Los Angeles.\n"
        f"Mission: Walk into that conference at 180 lbs.\n"
        f"Identity: Strong. Fit. Confident. Attracting Success.\n"
        f"Who are you becoming today, Dr. Rivera?"
    )
    send_vitality_signal(msg)

def routine_meditation():
    msg = (
        "🧘 05:10 AM | VISUALIZE THE WIN\n\n"
        "Close your eyes. See yourself in LA.\n"
        "See the suit fitting perfectly.\n"
        "Feel the handshake with the DeepMind/Google team.\n"
        "It is already done."
    )
    send_vitality_signal(msg)

def routine_caffeine_cut():
    msg = (
        "☕ 01:00 PM | CAFFEINE CUTOFF\n\n"
        "No more stimulants. Protect the recovery.\n"
        "Hydrate. The brain needs water, not jitters."
    )
    send_vitality_signal(msg)

def routine_sweat_equity():
    days = get_mission_status()
    msg = (
        f"🏋️ 06:00 PM | BUILD THE FUTURE\n\n"
        f"You have {days} days to carve the statue.\n"
        f"Target: 180 lbs. Lean. Dangerous.\n"
        f"35-40 min heavy weights. Do not negotiate with weakness."
    )
    send_vitality_signal(msg)

def routine_fasting_start():
    msg = (
        "🤐 08:00 PM | KITCHEN CLOSED\n\n"
        "Regeneration Mode: ON.\n"
        "You are disciplined. You are in control.\n"
        "Let the body burn fat while you rest."
    )
    send_vitality_signal(msg)

def routine_sleep_prep():
    msg = (
        "🌙 09:00 PM | SYSTEM SHUTDOWN\n\n"
        "Calories < 1800?\n"
        "Disconnect to Reconnect.\n"
        "Sleep is where the 4.0 upgrade happens.\n"
        "See you in the morning, Spartan."
    )
    send_vitality_signal(msg)

# --- THE SCHEDULER ---
schedule.every().day.at("17:00").do(routine_ignition)
schedule.every().day.at("05:10").do(routine_meditation)
schedule.every().day.at("13:00").do(routine_caffeine_cut)
schedule.every().day.at("18:00").do(routine_sweat_equity)
schedule.every().day.at("20:00").do(routine_fasting_start)
schedule.every().day.at("21:00").do(routine_sleep_prep)

print("---------------------------------------------------")
print("🤖 VITALITY COACH (FÉLIX 4.0) IS ONLINE")
print(f"🎯 TARGET: SBMT Conference (April 16, 2026)")
print("⏳ Waiting for the next scheduled event...")
print("---------------------------------------------------")

while True:
    schedule.run_pending()
    time.sleep(30)