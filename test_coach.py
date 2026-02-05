import streamlit as st
from twilio.rest import Client

# 1. Load Credentials
account_sid = st.secrets["twilio"]["account_sid"]
auth_token = st.secrets["twilio"]["auth_token"]
from_number = st.secrets["twilio"]["from_number"]
to_number = st.secrets["twilio"]["to_number"]

# 2. Handshake
client = Client(account_sid, auth_token)

# 3. Fire
print(f"Sending message from {from_number} to {to_number}...")
message = client.messages.create(
    body="Félix 4.0: The connection is live.",
    from_=from_number,
    to=to_number
)
print(f"Message sent! SID: {message.sid}")