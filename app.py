import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

# Set page config
st.set_page_config(page_title="💩 PoopLog", layout="wide", initial_sidebar_state="expanded")

# Custom CSS with the user's color palette
st.markdown("""
<style>
    :root {
        --primary: #8B4513;
        --secondary: #D2B48C;
        --background: #FFF8E7;
        --card-bg: #FAF3E0;
        --text-dark: #3B2F2F;
        --success: #7CFC00;
        --warning: #FFB347;
        --danger: #FF6347;
    }
    
    * {
        color: #3B2F2F;
    }
    
    body {
        background-color: #FFF8E7;
    }
    
    .stApp {
        background-color: #FFF8E7;
    }
    
    .main {
        background-color: #FFF8E7;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #FAF3E0;
        color: #3B2F2F;
        border-radius: 8px;
        padding: 10px 20px;
        margin-right: 5px;
        border: 2px solid #D2B48C;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #8B4513;
        color: #FFF8E7;
        border: 2px solid #8B4513;
    }
    
    .stButton > button {
        background-color: #8B4513;
        color: #FFF8E7;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background-color: #6B3410;
        color: #FFF8E7;
    }
    
    .stMetric {
        background-color: #FAF3E0;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #8B4513;
    }
    
    .stSelectbox, .stSlider, .stNumberInput, .stTextInput {
        background-color: #FAF3E0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #3B2F2F;
    }
    
    .stMarkdown {
        color: #3B2F2F;
    }
    
    .success-box {
        background-color: #E8F5E9;
        border-left: 4px solid #7CFC00;
        padding: 15px;
        border-radius: 8px;
        color: #3B2F2F;
    }
    
    .warning-box {
        background-color: #FFF3E0;
        border-left: 4px solid #FFB347;
        padding: 15px;
        border-radius: 8px;
        color: #3B2F2F;
    }
    
    .danger-box {
        background-color: #FFEBEE;
        border-left: 4px solid #FF6347;
        padding: 15px;
        border-radius: 8px;
        color: #3B2F2F;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'poop_data' not in st.session_state:
    st.session_state.poop_data = []

@st.cache_resource
@st.cache_resource
def get_google_sheets_client():
    """Connect to Google Sheets using Streamlit secrets"""
    try:
        credentials_dict = st.secrets["google_sheets_credentials"]

        # ✅ Add all required scopes for Sheets and Drive
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.readonly"
        ]

        credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        client = gspread.authorize(credentials)
        return client

    except Exception as e:
        st.error(f"❌ Error connecting to Google Sheets: {e}")
        st.info("📌 Please check your Streamlit secrets or service account setup.")
        return None


def get_worksheet():
    """Get or create the PoopLog worksheet"""
    client = get_google_sheets_client()
    if client is None:
        return None

    try:
        # ✅ Try to open the spreadsheet
        sheet = client.open("PoopLog")
    except gspread.exceptions.SpreadsheetNotFound:
        try:
            # ✅ Create spreadsheet if it doesn’t exist
            sheet = client.create("PoopLog")

            # ✅ Share it automatically with the service account for safety
            client.insert_permission(
                sheet.id,
                None,
                perm_type="anyone",
                role="writer"
            )

            worksheet = sheet.get_worksheet(0)
            worksheet.append_row(['Date', 'User', 'Ease', 'Notes'])
            return worksheet
        except Exception as e:
            st.error(f"❌ Could not create Google Sheet: {e}")
            return None

    # ✅ Return first worksheet if exists
    return sheet.get_worksheet(0)

# def get_google_sheets_client():
#     """Connect to Google Sheets using Streamlit secrets"""
#     try:
#         credentials_dict = st.secrets["google_sheets_credentials"]
#         credentials = Credentials.from_service_account_info(
#             credentials_dict,
#             scopes=['https://www.googleapis.com/auth/spreadsheets']
#         )
#         return gspread.authorize(credentials)
#     except Exception as e:
#         st.error(f"❌ Error connecting to Google Sheets: {e}")
#         st.info("📌 Please add your Google Sheets credentials to Streamlit secrets.")
#         return None

# def get_worksheet():
#     """Get the PoopLog worksheet from Google Sheets"""
#     client = get_google_sheets_client()
#     if client is None:
#         return None
    
#     try:
#         # Try to open existing sheet
#         sheet = client.open("PoopLog")
#     except gspread.exceptions.SpreadsheetNotFound:
#         # Create new sheet if it doesn't exist
#         sheet = client.create("PoopLog")
#         worksheet = sheet.get_worksheet(0)
#         worksheet.append_row(['Date', 'User', 'Ease', 'Notes'])
#         return worksheet
    
#     return sheet.get_worksheet(0)

def load_data():
    """Load data from Google Sheets"""
    worksheet = get_worksheet()
    if worksheet is None:
        return pd.DataFrame(columns=['Date', 'User', 'Ease', 'Notes'])
    
    try:
        data = worksheet.get_all_records()
        if not data:
            return pd.DataFrame(columns=['Date', 'User', 'Ease', 'Notes'])
        
        df = pd.DataFrame(data)
        # Convert Ease column to float
        if 'Ease' in df.columns:
            df['Ease'] = pd.to_numeric(df['Ease'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=['Date', 'User', 'Ease', 'Notes'])

def save_data(date, user, ease, notes):
    """Save a new entry to Google Sheets"""
    worksheet = get_worksheet()
    if worksheet is None:
        st.error("Cannot connect to Google Sheets")
        return False
    
    try:
        worksheet.append_row([str(date), user, str(ease), notes])
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def delete_entry(date, user):
    """Delete an entry from Google Sheets"""
    worksheet = get_worksheet()
    if worksheet is None:
        return False
    
    try:
        data = worksheet.get_all_records()
        for idx, row in enumerate(data, start=2):  # Start at 2 because row 1 is header
            if row['Date'] == str(date) and row['User'] == user:
                worksheet.delete_rows(idx)
                return True
        return False
    except Exception as e:
        st.error(f"Error deleting entry: {e}")
        return False

# Get current week dates
def get_week_dates():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    dates = [monday + timedelta(days=i) for i in range(7)]
    return dates

# Main app
st.title("💩 PoopLog – Your Weekly Dump Tracker")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📋 Settings")
    user = st.radio("Select User:", ["Me", "Friend"], horizontal=True)
    
    week_dates = get_week_dates()
    week_start = week_dates[0].strftime("%b %d")
    week_end = week_dates[6].strftime("%b %d, %Y")
    st.markdown(f"**Current Week:** {week_start} - {week_end}")

# Load existing data
df = load_data()

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Log Entry", "📊 This Week's Comparison", "📈 All-Time Stats"])

with tab1:
    st.subheader(f"Log Entry for {user}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entry_date = st.date_input("Select Date:", value=datetime.now())
    
    with col2:
        ease = st.slider("Ease Level (0=Hard, 1=Easy):", 0.0, 1.0, 0.5, 0.1)
    
    notes = st.text_area("Notes (optional):", placeholder="How was it? Any comments?")
    
    if st.button("💾 Save Entry", use_container_width=True):
        existing = df[(df['Date'] == str(entry_date)) & (df['User'] == user)]
        
        if not existing.empty:
            delete_entry(entry_date, user)
        
        if save_data(entry_date, user, ease, notes):
            st.success(f"✅ Entry saved for {user} on {entry_date}!")
            st.rerun()
        else:
            st.error("Failed to save entry")

with tab2:
    st.subheader("This Week's Comparison")
    
    # Filter data for current week
    week_dates = get_week_dates()
    week_start = week_dates[0]
    week_end = week_dates[6]
    
    week_data = df[(pd.to_datetime(df['Date']) >= week_start) & (pd.to_datetime(df['Date']) <= week_end)]
    
    if len(week_data) > 0:
        # Categorize as easy or average
        week_data['Category'] = week_data['Ease'].apply(lambda x: 'Easy' if x >= 0.5 else 'Average')
        
        # Count by user and category
        comparison = week_data.groupby(['User', 'Category']).size().unstack(fill_value=0)
        
        # Create Plotly bar chart
        fig = go.Figure()
        
        for user_name in comparison.index:
            easy_count = comparison.loc[user_name, 'Easy'] if 'Easy' in comparison.columns else 0
            avg_count = comparison.loc[user_name, 'Average'] if 'Average' in comparison.columns else 0
            
            fig.add_trace(go.Bar(
                name=user_name,
                x=['Easy Poops 😎', 'Average Poops 😐'],
                y=[easy_count, avg_count],
                marker_color=['#7CFC00', '#FFB347'],
                text=[easy_count, avg_count],
                textposition='auto',
            ))
        
        fig.update_layout(
            title="Weekly Poop Comparison",
            xaxis_title="Poop Category",
            yaxis_title="Count",
            barmode='group',
            plot_bgcolor='#FAF3E0',
            paper_bgcolor='#FFF8E7',
            font=dict(color='#3B2F2F', size=12),
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Weekly stats table
        st.markdown("**Weekly Breakdown:**")
        st.dataframe(week_data[['Date', 'User', 'Ease', 'Notes']].sort_values('Date'), use_container_width=True)
    else:
        st.info("📭 No entries logged this week yet. Start logging to see comparisons!")

with tab3:
    st.subheader("All-Time Statistics")
    
    if len(df) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_entries = len(df)
            st.metric("Total Entries", total_entries, "💩")
        
        with col2:
            me_entries = len(df[df['User'] == 'Me'])
            st.metric("Your Entries", me_entries, "👤")
        
        with col3:
            friend_entries = len(df[df['User'] == 'Friend'])
            st.metric("Friend's Entries", friend_entries, "👥")
        
        with col4:
            avg_ease = df['Ease'].mean()
            st.metric("Avg Ease", f"{avg_ease:.2f}", "📊")
        
        st.markdown("---")
        
        # All-time comparison
        df['Category'] = df['Ease'].apply(lambda x: 'Easy' if x >= 0.5 else 'Average')
        all_time = df.groupby(['User', 'Category']).size().unstack(fill_value=0)
        
        fig2 = go.Figure()
        
        for user_name in all_time.index:
            easy_count = all_time.loc[user_name, 'Easy'] if 'Easy' in all_time.columns else 0
            avg_count = all_time.loc[user_name, 'Average'] if 'Average' in all_time.columns else 0
            
            fig2.add_trace(go.Bar(
                name=user_name,
                x=['Easy Poops 😎', 'Average Poops 😐'],
                y=[easy_count, avg_count],
                marker_color=['#7CFC00', '#FFB347'],
                text=[easy_count, avg_count],
                textposition='auto',
            ))
        
        fig2.update_layout(
            title="All-Time Poop Comparison",
            xaxis_title="Poop Category",
            yaxis_title="Count",
            barmode='group',
            plot_bgcolor='#FAF3E0',
            paper_bgcolor='#FFF8E7',
            font=dict(color='#3B2F2F', size=12),
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("📭 No data yet. Start logging entries to see statistics!")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #8B4513; font-size: 12px;'>Made with Kakka by Saagar for Nikhil</p>", unsafe_allow_html=True)




# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import os
# import random

# # Page config
# st.set_page_config(page_title="💩 PoopLog", layout="wide", initial_sidebar_state="expanded")

# st.markdown("""
#     <style>
#     :root {
#         --primary-brown: #8B4513;
#         --secondary-tan: #D2B48C;
#         --background: #FFF8E7;
#         --card-bg: #FAF3E0;
#         --dark-text: #3B2F2F;
#         --success-green: #7CFC00;
#         --warning-orange: #FFB347;
#         --danger-red: #FF6347;
#     }
    
#     * {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }
    
#     .main {
#         background-color: #FFF8E7;
#     }
    
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 2px;
#         background-color: transparent;
#     }
    
#     .stTabs [data-baseweb="tab-list"] button {
#         background-color: #FAF3E0;
#         color: #3B2F2F;
#         font-weight: 600;
#         border-radius: 8px 8px 0 0;
#         border: none;
#         padding: 12px 24px;
#         font-size: 15px;
#         transition: all 0.3s ease;
#     }
    
#     .stTabs [data-baseweb="tab-list"] button:hover {
#         background-color: #F5EDD8;
#     }
    
#     .stTabs [aria-selected="true"] {
#         background-color: #8B4513 !important;
#         color: white !important;
#         box-shadow: 0 2px 8px rgba(139, 69, 19, 0.2);
#     }
    
#     h1 {
#         color: #3B2F2F;
#         font-size: 2.5em;
#         font-weight: 700;
#         letter-spacing: -0.5px;
#         margin-bottom: 8px;
#     }
    
#     h2 {
#         color: #8B4513;
#         font-size: 1.8em;
#         font-weight: 600;
#         margin-top: 24px;
#         margin-bottom: 16px;
#     }
    
#     h3 {
#         color: #8B4513;
#         font-size: 1.3em;
#         font-weight: 600;
#     }
    
#     h4 {
#         color: #8B4513;
#         font-weight: 600;
#     }
    
#     .subtitle {
#         color: #D2B48C;
#         font-size: 1.1em;
#         font-weight: 500;
#         margin-bottom: 24px;
#     }
    
#     .metric-card {
#         background: linear-gradient(135deg, #FAF3E0 0%, #FFF8E7 100%);
#         padding: 20px;
#         border-radius: 12px;
#         border: 1px solid #E8DCC8;
#         box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
#         transition: all 0.3s ease;
#     }
    
#     .metric-card:hover {
#         box-shadow: 0 4px 12px rgba(139, 69, 19, 0.1);
#         border-color: #8B4513;
#     }
    
#     .stButton > button {
#         background-color: #8B4513;
#         color: white;
#         border: none;
#         border-radius: 8px;
#         padding: 12px 24px;
#         font-weight: 600;
#         font-size: 15px;
#         transition: all 0.3s ease;
#         box-shadow: 0 2px 8px rgba(139, 69, 19, 0.2);
#     }
    
#     .stButton > button:hover {
#         background-color: #6B3410;
#         box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
#         transform: translateY(-2px);
#     }
    
#     .stSlider > div > div > div > div {
#         background-color: #8B4513;
#     }
    
#     .stTextInput > div > div > input {
#         border-color: #D2B48C;
#         border-radius: 8px;
#         background-color: #FFFBF5;
#     }
    
#     .stTextArea > div > div > textarea {
#         border-color: #D2B48C;
#         border-radius: 8px;
#         background-color: #FFFBF5;
#     }
    
#     .stDateInput > div > div > input {
#         border-color: #D2B48C;
#         border-radius: 8px;
#         background-color: #FFFBF5;
#     }
    
#     .stRadio > div > label {
#         color: #3B2F2F;
#         font-weight: 500;
#     }
    
#     .stSuccess {
#         background-color: #F0FFE0;
#         border-color: #7CFC00;
#         border-radius: 8px;
#         color: #3B2F2F;
#     }
    
#     .stInfo {
#         background-color: #FFF9E6;
#         border-color: #D2B48C;
#         border-radius: 8px;
#         color: #3B2F2F;
#     }
    
#     .stWarning {
#         background-color: #FFF3E0;
#         border-color: #FFB347;
#         border-radius: 8px;
#         color: #3B2F2F;
#     }
    
#     .stError {
#         background-color: #FFE6E6;
#         border-color: #FF6347;
#         border-radius: 8px;
#         color: #3B2F2F;
#     }
    
#     .stDivider {
#         border-color: #E8DCC8;
#     }
    
#     .sidebar .stRadio > div > label {
#         font-size: 16px;
#         font-weight: 600;
#         color: #3B2F2F;
#     }
    
#     .sidebar .stCaption {
#         color: #8B4513;
#         font-size: 14px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # CSV file path
# CSV_FILE = "poop_log.csv"

# # Initialize or load CSV
# def load_data():
#     if os.path.exists(CSV_FILE):
#         return pd.read_csv(CSV_FILE)
#     return pd.DataFrame(columns=["Date", "User", "Viscosity", "Ease", "Notes"])

# def save_data(df):
#     df.to_csv(CSV_FILE, index=False)

# def get_current_week():
#     today = datetime.now()
#     monday = today - timedelta(days=today.weekday())
#     sunday = monday + timedelta(days=6)
#     return monday, sunday

# def get_day_name(date_obj):
#     days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#     return days[date_obj.weekday()]

# # Funny messages
# def get_funny_message(viscosity, ease, frequency):
#     messages = [
#         f"💩 You're on a roll! {frequency} dumps this week!",
#         f"🚽 Ease level: {ease:.1f}/1 — {'Smooth sailing!' if ease < 0.5 else 'Time to eat more fiber 🥦'}",
#         f"🌊 Viscosity: {viscosity:.1f}/10 — {'Waterfall mode activated!' if viscosity < 3 else 'Rock solid performance!' if viscosity > 7 else 'Perfectly balanced.'}",
#         "💪 Keep up the good work, champion!",
#         "🎯 Your digestive system is on point!",
#         "🔥 That's what I call a productive day!",
#     ]
#     return random.choice(messages)

# # Poop emoji reactions
# def get_poop_reaction():
#     reactions = ["💩", "🚽", "💦", "🌊", "🔥", "⚡", "🎉", "👑"]
#     return " ".join(random.choices(reactions, k=3))

# # Main title
# col1, col2, col3 = st.columns([1, 2, 1])
# with col2:
#     st.markdown("<h1 style='text-align: center;'>💩 PoopLog</h1>", unsafe_allow_html=True)
#     st.markdown("<p class='subtitle' style='text-align: center;'>Weekly Dump Tracker for You & Your Friend</p>", unsafe_allow_html=True)

# st.divider()

# # Sidebar
# st.sidebar.markdown("### 👤 User Selection")
# current_user = st.sidebar.radio("Who are you?", ["Me", "Friend"], horizontal=True)

# # Get current week
# monday, sunday = get_current_week()
# st.sidebar.markdown("---")
# st.sidebar.markdown("### 📅 Current Week")
# st.sidebar.caption(f"**{monday.strftime('%b %d')}** → **{sunday.strftime('%b %d, %Y')}**")

# # Tabs
# tab1, tab2, tab3 = st.tabs(["📝 Log Entry", "📊 Weekly Comparison", "🏆 Leaderboard"])

# # ============ TAB 1: LOG ENTRY ============
# with tab1:
#     st.markdown("### Record Your Daily Dump")
#     st.markdown(f"**Logging as:** {current_user}", unsafe_allow_html=True)
#     st.divider()
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         log_date = st.date_input("📅 Date", value=datetime.now(), label_visibility="collapsed")
    
#     with col2:
#         st.write("")  # Spacing
    
#     st.markdown("#### 💧 Viscosity Level")
#     st.caption("How thick or watery was it?")
#     viscosity = st.slider("Viscosity", 0, 10, 5, 
#                           help="0 = Waterfall | 10 = Rock Solid",
#                           format="%d", label_visibility="collapsed")
    
#     viscosity_labels = {0: "🌊 Waterfall", 5: "🟡 Medium", 10: "🪨 Rock Solid"}
#     st.caption(f"**Current:** {viscosity_labels.get(viscosity, f'{viscosity}/10')}")
    
#     st.markdown("#### 🚽 Ease Level")
#     st.caption("How easy was it to go?")
#     ease = st.slider("Ease", 0.0, 1.0, 0.5, step=0.1,
#                      help="0 = Smooth | 1 = Struggle", label_visibility="collapsed")
    
#     ease_labels = {0.0: "✨ Smooth", 0.5: "🟡 Medium", 1.0: "😤 Struggle"}
#     st.caption(f"**Current:** {ease_labels.get(ease, f'{ease:.1f}')}")
    
#     st.markdown("#### 📝 Notes")
#     notes = st.text_area("Add any additional details (optional)", placeholder="Be creative! 😄", label_visibility="collapsed", height=100)
    
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         if st.button("💾 Save Log Entry", use_container_width=True, type="primary"):
#             df = load_data()
#             new_entry = pd.DataFrame({
#                 "Date": [log_date.strftime("%Y-%m-%d")],
#                 "User": [current_user],
#                 "Viscosity": [viscosity],
#                 "Ease": [ease],
#                 "Notes": [notes]
#             })
#             df = pd.concat([df, new_entry], ignore_index=True)
#             save_data(df)
            
#             # Funny reaction
#             st.success(f"✅ Log saved! {get_poop_reaction()}")
            
#             # Get frequency for current user this week
#             df["Date"] = pd.to_datetime(df["Date"])
#             week_logs = len(df[(df["User"] == current_user) & (df["Date"] >= monday) & (df["Date"] <= sunday)])
            
#             st.info(get_funny_message(viscosity, ease, week_logs))
#             st.balloons()

# # ============ TAB 2: WEEKLY COMPARISON ============
# with tab2:
#     df = load_data()
    
#     if len(df) == 0:
#         st.warning("📭 No logs yet! Start tracking to see the comparison.")
#     else:
#         df["Date"] = pd.to_datetime(df["Date"])
        
#         week_data = df[(df["Date"] >= monday) & (df["Date"] <= sunday)]
        
#         if len(week_data) == 0:
#             st.info("📭 No logs for this week yet. Start logging to see the comparison!")
#         else:
#             st.markdown("### 📊 This Week's Comparison")
#             st.divider()
            
#             week_data = week_data.copy()
#             week_data["Poop_Type"] = week_data["Ease"].apply(lambda x: "Easy" if x < 0.5 else "Average")
            
#             comparison_data = week_data.groupby(["User", "Poop_Type"]).size().reset_index(name="Count")
            
#             fig = go.Figure()
            
#             for user in ["Me", "Friend"]:
#                 user_data = comparison_data[comparison_data["User"] == user]
#                 easy_count = user_data[user_data["Poop_Type"] == "Easy"]["Count"].values
#                 avg_count = user_data[user_data["Poop_Type"] == "Average"]["Count"].values
                
#                 easy_count = easy_count[0] if len(easy_count) > 0 else 0
#                 avg_count = avg_count[0] if len(avg_count) > 0 else 0
                
#                 color = "#8B4513" if user == "Me" else "#D2B48C"
                
#                 fig.add_trace(go.Bar(
#                     name=user,
#                     x=["Easy Poop", "Average Poop"],
#                     y=[easy_count, avg_count],
#                     marker_color=color,
#                     marker_line_color='white',
#                     marker_line_width=2,
#                     hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
#                 ))
            
#             fig.update_layout(
#                 title={
#                     'text': "Easy vs Average Poops This Week",
#                     'x': 0.5,
#                     'xanchor': 'center',
#                     'font': {'size': 20, 'color': '#3B2F2F'}
#                 },
#                 xaxis_title="Poop Type",
#                 yaxis_title="Count",
#                 barmode="group",
#                 plot_bgcolor='#FFF8E7',
#                 paper_bgcolor='#FAF3E0',
#                 hovermode='x unified',
#                 font=dict(family="Segoe UI, sans-serif", size=12, color="#3B2F2F"),
#                 xaxis=dict(showgrid=False, zeroline=False),
#                 yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#E8DCC8', zeroline=False),
#                 margin=dict(l=50, r=50, t=80, b=50),
#                 height=400
#             )
            
#             st.plotly_chart(fig, use_container_width=True)
            
#             st.divider()
            
#             st.markdown("### 📅 Daily Breakdown (Mon-Sun)")
            
#             daily_data = []
#             for i in range(7):
#                 current_day = monday + timedelta(days=i)
#                 day_name = get_day_name(current_day)
                
#                 me_logs = week_data[(week_data["User"] == "Me") & (week_data["Date"].dt.date == current_day.date())]
#                 friend_logs = week_data[(week_data["User"] == "Friend") & (week_data["Date"].dt.date == current_day.date())]
                
#                 me_easy = len(me_logs[me_logs["Poop_Type"] == "Easy"])
#                 me_avg = len(me_logs[me_logs["Poop_Type"] == "Average"])
#                 friend_easy = len(friend_logs[friend_logs["Poop_Type"] == "Easy"])
#                 friend_avg = len(friend_logs[friend_logs["Poop_Type"] == "Average"])
                
#                 daily_data.append({
#                     "Day": day_name,
#                     "Me (Easy)": me_easy,
#                     "Me (Avg)": me_avg,
#                     "Friend (Easy)": friend_easy,
#                     "Friend (Avg)": friend_avg
#                 })
            
#             daily_df = pd.DataFrame(daily_data)
#             st.dataframe(daily_df, use_container_width=True, hide_index=True)
            
#             st.divider()
            
#             st.markdown("### 📈 Weekly Stats")
            
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.markdown("#### 👤 Me")
#                 me_data = week_data[week_data["User"] == "Me"]
#                 if len(me_data) > 0:
#                     metric_col1, metric_col2, metric_col3 = st.columns(3)
#                     with metric_col1:
#                         st.metric("Total Dumps", len(me_data))
#                     with metric_col2:
#                         st.metric("Avg Viscosity", f"{me_data['Viscosity'].mean():.1f}/10")
#                     with metric_col3:
#                         st.metric("Avg Ease", f"{me_data['Ease'].mean():.2f}/1")
#                 else:
#                     st.info("No logs yet")
            
#             with col2:
#                 st.markdown("#### 👥 Friend")
#                 friend_data = week_data[week_data["User"] == "Friend"]
#                 if len(friend_data) > 0:
#                     metric_col1, metric_col2, metric_col3 = st.columns(3)
#                     with metric_col1:
#                         st.metric("Total Dumps", len(friend_data))
#                     with metric_col2:
#                         st.metric("Avg Viscosity", f"{friend_data['Viscosity'].mean():.1f}/10")
#                     with metric_col3:
#                         st.metric("Avg Ease", f"{friend_data['Ease'].mean():.2f}/1")
#                 else:
#                     st.info("No logs yet")

# # ============ TAB 3: LEADERBOARD ============
# with tab3:
#     df = load_data()
    
#     if len(df) == 0:
#         st.warning("📭 No logs yet! Start tracking to compete.")
#     else:
#         st.markdown("### 🏆 All-Time Leaderboard")
        
#         df["Date"] = pd.to_datetime(df["Date"])
        
#         user_stats = df.groupby("User").agg({
#             "Viscosity": "mean",
#             "Ease": "mean",
#             "Date": "count"
#         }).rename(columns={"Date": "Total Dumps"}).round(2)
        
#         user_stats = user_stats.sort_values("Total Dumps", ascending=False)
        
#         st.dataframe(user_stats, use_container_width=True)
        
#         st.divider()
        
#         st.markdown("### 🎯 This Week's Leaderboard")
        
#         week_data = df[(df["Date"] >= monday) & (df["Date"] <= sunday)]
        
#         if len(week_data) > 0:
#             week_stats = week_data.groupby("User").agg({
#                 "Viscosity": "mean",
#                 "Ease": "mean",
#                 "Date": "count"
#             }).rename(columns={"Date": "Dumps This Week"}).round(2)
            
#             week_stats = week_stats.sort_values("Dumps This Week", ascending=False)
            
#             st.dataframe(week_stats, use_container_width=True)
#         else:
#             st.info("No logs for this week yet!")
