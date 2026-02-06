import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Vitality Engine 4.0", page_icon="⚡", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🦁 The Identity")
    st.markdown("**You are an Architect.**")
    st.markdown("**You are a Future Google Leader.**")
    st.divider()
    
    target_date = date(2026, 4, 16)
    today = date.today()
    delta = target_date - today
    st.metric(label="Days to SBMT (Los Angeles)", value=f"{delta.days}")
    st.info("Target Weight: **185 lbs**")

# --- DATABASE CONNECTION ---
@st.cache_resource
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("Vitality_Engine_DB") 
    return spreadsheet.worksheet("Daily_Logs")

# --- MAIN DASHBOARD ---
st.title("⚡ Vitality Engine 4.0")
st.caption(f"Tracking Active. Date: {today.strftime('%B %d, %Y')}")

# --- INPUT FORM ---
st.subheader("📝 Daily Log")
with st.form(key="entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        date_entry = st.date_input("Date", value=today)
        weight = st.number_input("Weight (lbs)", min_value=0.0, format="%.1f")
        calories = st.number_input("Calories In", min_value=0, step=50)
        wake_time = st.time_input("Wake Time (Target 05:00)", value=datetime.strptime("05:00", "%H:%M").time())
        sleep_time = st.time_input("Sleep Time", value=datetime.strptime("21:30", "%H:%M").time())

    with col2:
        st.write("Habit Stack")
        meditation = st.checkbox("🧘 Meditation (5:10 AM)")
        caffeine = st.checkbox("☕ Caffeine Cutoff (1 PM)")
        workout = st.checkbox("🏋️ Workout (6 PM)")
        fasting = st.checkbox("🤐 Fasting (8 PM)")
        energy = st.slider("Energy Level (1-10)", 1, 10, 8)
    
    notes = st.text_area("Mindset Notes", placeholder="Who did you become today?")
    
    if st.form_submit_button("🚀 COMMIT TO DATABASE"):
        try:
            sheet = get_sheet()
            row = [
                str(date_entry), weight, calories, str(wake_time), 
                meditation, caffeine, workout, fasting, 
                str(sleep_time), energy, notes
            ]
            sheet.append_row(row)
            st.success("✅ Data Secured in Cloud.")
            st.cache_data.clear()
        except Exception as e:
            st.error(f"Error: {e}")

# --- DATA VIEW & CLEANING (THE FIX) ---
try:
    sheet = get_sheet()
    df = pd.DataFrame(sheet.get_all_records())
    
    # 🧼 CLEANING PROTOCOL: Force all numbers to be numbers
    # If it's text/garbage, it becomes NaN (Safe for graphs)
    cols_to_clean = ['Weight_lbs', 'Calories_In', 'Energy_Level']
    
    for col in cols_to_clean:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    st.divider()
    
    col_graph, col_data = st.columns([2, 1])

    with col_graph:
        st.subheader("📉 The Trend")
        if not df.empty and 'Weight_lbs' in df.columns:
            clean_df = df.dropna(subset=['Weight_lbs'])
            st.line_chart(clean_df, x="Date", y="Weight_lbs")
        else:
            st.info("No data yet.")

    with col_data:
        st.subheader("📋 History")
        st.dataframe(df.tail(5))

except Exception as e:
    st.warning("Waiting for Database Connection...")
    st.error(f"Debug Info: {e}")