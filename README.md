# Mood of the Queue

A simple internal tool for logging and visualizing the mood of the support ticket queue throughout the day. Built with Streamlit, Google Sheets, and Plotly.

## Purpose

This app helps support agents quickly log the mood of the ticket queue (e.g., 😊 😠 😕 🎉) and visualize emotional trends over time. It enables:
- Fast mood logging with optional notes
- Visualization of mood trends (bar charts, time series)
- Filtering and grouping by date
- Easy review of all logged moods

## Features

- **Log a Mood:**  
  Select a mood (emoji) and optionally add a note. Each entry is timestamped and saved to a Google Sheet.

- **Flexible Filtering:**  
  Use the sidebar to filter mood entries by any date range. This allows you to focus on a single day, a week, or any custom period.

- **Visualizations:**  
  - **Bar Chart:**  
    See the count of each mood for the selected date range.  
    Optionally, group by day to see how mood counts change over multiple days.
  - **Time Series (Mood Timeline):**  
    Visualize how moods change throughout the day. Each mood entry is plotted at its timestamp, so you can see the sequence and timing of mood changes.
  - **Mood Counts by Hour (optional):**  
    (You can add this if you wish) See which moods are most common at different hours of the day.

- **Data Table:**  
  View a table of all mood entries that match your current filter. This makes it easy to review notes and see the full log.

## Usage

- **Log Mood:**  
  Select a mood and add a note, then click "Log Mood" to save your entry.

- **Filter by Date:**  
  Use the sidebar to select a start and end date. All visualizations and the data table will update to reflect your selection.

- **Group by Day:**  
  Toggle the "Group by day" checkbox in the sidebar to see mood counts for each day in your selected range.

- **Visualizations:**  
  - The **bar chart** shows mood counts for your selected range or grouped by day.
  - The **time series plot** (Mood Timeline) shows the sequence and timing of mood changes throughout the day.
  - The **data table** displays all filtered mood logs, including timestamps and notes.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Mochi_Health
```

### 2. Install Dependencies
It is recommended to use a virtual environment (e.g., conda or venv).
```bash
pip install streamlit gspread google-auth pandas plotly
```

### 3. Google Sheets Integration
1. **Create a Google Sheet** with columns: `Timestamp`, `Mood`, `Note`.
2. **Create a Google Service Account** in Google Cloud Console.
3. **Download the credentials JSON** and place it in the project directory as `credentials.json`.
4. **Share your Google Sheet** with the service account's `client_email` (found in the JSON file).
5. **Update `SHEET_ID`** in `app.py` with your sheet's ID (the long string in the URL).

### 4. Run the App
```bash
streamlit run app.py
```
The app will open in your browser.

## Troubleshooting
- **FileNotFoundError for credentials.json:**
  - Ensure `credentials.json` is in the same directory as `app.py`.
- **Google Sheets 404 error:**
  - Double-check the `SHEET_ID` (should be just the ID, not the full URL)
  - Make sure the sheet is shared with the service account email
  - Ensure the worksheet/tab name matches `SHEET_NAME` in `app.py`
- **No data appears:**
  - Make sure your Google Sheet has the correct columns and is not empty

## Customization
- You can add more moods by editing the `moods` dictionary in `app.py`.
- To change the default worksheet, update `SHEET_NAME`.

