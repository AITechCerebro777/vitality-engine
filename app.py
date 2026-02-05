import sys
import subprocess
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
# --- BACKGROUND COACH STARTUP ---
@st.cache_resource
def start_vitality_coach():
    """Checks if the Coach is running, and if not, kicks it awake."""
    cmd = [sys.executable, "coach.py"]
    subprocess.Popen(cmd)
    return "Coach Running"

# Fire the engine
start_vitality_coach()
# -------------------------------

# --- CONFIGURATION ---
st.set_page_config(page_title="Vitality Engine", page_icon="⚡", layout="wide")
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SHEET_NAME = "Vitality_Engine_DB"
TAB_NAME = "Daily_Logs"

# --- BACKEND FUNCTIONS ---
def get_connection():
    """Connects to Google Sheets (Handles both Cloud and Local)"""
    try:
        # 1. Try to grab credentials from Streamlit Cloud Secrets
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    except:
        # 2. Fallback to Local File (for your laptop)
        creds = ServiceAccountCredentials.from_json_keyfile_name("vitality_key.json", SCOPE)
    
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).worksheet(TAB_NAME)

def load_data():
    sheet = get_connection()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_entry(date_val, weight, calories, wake, med, caff, work, fast, sleep, energy, notes):
    sheet = get_connection()
    new_row = [str(date_val), weight, calories, str(wake), med, caff, work, fast, str(sleep), energy, notes]
    sheet.append_row(new_row)

# --- SIDEBAR: THE NORTH STAR ---
with st.sidebar:
    st.header("🦁 The Identity")
    st.markdown("You are an **Architect**.")
    st.markdown("You are a **Future Google Leader**.")
    
    # Calculate Days Remaining
    today = date.today()
    sbmt_date = date(2026, 4, 14)
    retreat_date = date(2026, 5, 11)
    
    days_to_sbmt = (sbmt_date - today).days
    
    st.divider()
    st.metric(label="⏳ Days to SBMT (Los Angeles)", value=days_to_sbmt)
    st.divider()
    st.info("Target Weight: **185 lbs**")

# --- MAIN PAGE ---
st.title("⚡ Vitality Engine 4.0")
st.caption(f"Tracking system active. Date: {datetime.now().strftime('%B %d, %Y')}")

# 1. THE COCKPIT
with st.form("entry_form", clear_on_submit=True):
    st.subheader("📝 Daily Log")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_input = st.date_input("Date", datetime.now())
        weight_input = st.number_input("Weight (lbs)", min_value=0.0, format="%.1f")
        cal_input = st.number_input("Calories", min_value=0)
    
    with col2:
        wake_input = st.time_input("Wake Time (Target 05:00)", datetime.strptime("05:00", "%H:%M"))
        energy_input = st.slider("Energy Level (1-10)", 1, 10, 8)
        sleep_input = st.time_input("Sleep Time", datetime.strptime("21:00", "%H:%M"))

    with col3:
        st.markdown("**Habit Stack**")
        med_input = st.checkbox("🧘 Meditation")
        caff_input = st.checkbox("☕ Caffeine Cutoff")
        work_input = st.checkbox("💪 Workout")
        fast_input = st.checkbox("🤐 Fasting")

    notes_input = st.text_area("Notes / Mindset")
    
    submitted = st.form_submit_button("🚀 COMMIT TO DATABASE")

    if submitted:
        try:
            save_entry(date_input, weight_input, cal_input, wake_input, 
                      med_input, caff_input, work_input, fast_input, 
                      sleep_input, energy_input, notes_input)
            st.toast("✅ Success! Data Logged.")
        except Exception as e:
            st.error(f"Error: {e}")

# 2. THE ANALYTICS
st.divider()
col_left, col_right = st.columns([2, 1])

try:
    df = load_data()
    df['Date'] = pd.to_datetime(df['Date'])
    
    with col_left:
        st.subheader("📉 The Trend")
        st.line_chart(df.set_index('Date')['Weight_lbs'])
        
    with col_right:
        st.subheader("📋 Recent History")
        display_cols = ['Date', 'Weight_lbs', 'Calories_In']
        st.dataframe(df[display_cols].tail(10), hide_index=True)

except Exception as e:
    st.info("Awaiting data connection...")