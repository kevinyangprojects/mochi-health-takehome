import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date


# --- Google Sheets Setup ---
SHEET_ID = '1B2D4QhXlcvcw5pA9gzxIj4I--y44uytU4YDRIa1i6qA'
SHEET_NAME = 'Sheet1'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Load credentials from Streamlit secrets
creds_dict = st.secrets["google_service_account"]
CREDS = Credentials.from_service_account_info(dict(creds_dict), scopes=SCOPES)

gc = gspread.authorize(CREDS)
sheet = gc.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# --- Mood Logging UI ---
st.title("Mood of the Queue")
moods = {"😊": "Happy", "😠": "Frustrated", "😕": "Confused", "🎉": "Joyful"}
mood = st.selectbox("Select mood", options=list(moods.keys()))
note = st.text_input("Add a note (optional)")
if st.button("Log Mood"):
    timestamp = datetime.now().isoformat()
    sheet.append_row([timestamp, mood, note])
    st.success("Mood logged!")

# --- Visualization ---
data = pd.DataFrame(sheet.get_all_records())
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# --- Filtering Controls ---
st.sidebar.header("Filter Options")
min_date = data['Timestamp'].min().date() if not data.empty else date.today()
max_date = data['Timestamp'].max().date() if not data.empty else date.today()
date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple):
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

filtered_data = data[(data['Timestamp'].dt.date >= start_date) & (data['Timestamp'].dt.date <= end_date)]

# --- Grouping Option ---
group_by_day = st.sidebar.checkbox("Group by day", value=False)

if group_by_day:
    st.subheader("Mood Counts by Day")
    grouped = filtered_data.groupby([filtered_data['Timestamp'].dt.date, 'Mood']).size().reset_index(name='Count')
    fig = px.bar(
        grouped,
        x='Timestamp',
        y='Count',
        color='Mood',
        barmode='group',
        title="Mood Counts by Day"
    )
else:
    st.subheader("Mood Counts for Selected Range")
    mood_counts = filtered_data['Mood'].value_counts().reset_index()
    mood_counts.columns = ['Mood', 'Count']
    fig = px.bar(mood_counts, x='Mood', y='Count', title="Mood Counts for Selected Range")

st.plotly_chart(fig)

# --- Mood Over Time (for selected date range) ---
if not filtered_data.empty:
    st.subheader("Mood Changes Throughout the Day")
    # Sort by timestamp for proper plotting
    filtered_data = filtered_data.sort_values('Timestamp')
    fig_time = px.scatter(
        filtered_data,
        x='Timestamp',
        y='Mood',
        color='Mood',
        symbol='Mood',
        title="Mood Timeline",
        labels={'Timestamp': 'Time', 'Mood': 'Mood'},
        height=400
    )
    st.plotly_chart(fig_time)
else:
    st.info("No data for the selected range to plot mood changes over time.")

# --- Table of all moods ---
st.subheader("Filtered Logged Moods")
st.dataframe(filtered_data)