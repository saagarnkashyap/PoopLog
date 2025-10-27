💩 PoopLog – The Weekly Ease Tracker

“Because every smooth journey deserves recognition.”
Track. Compare. Reflect. 💩

🧠 Overview

PoopLog is a Streamlit-based web app designed for ultimate bowel accountability between friends.
It syncs data from a shared Google Sheet, turning daily dumps into delightful data visualizations.

It’s part science, part fun — and entirely serious about gut progress.
Watch your ease scores evolve through clean plots, summaries, and weekly leaderboards!

✨ Features

✅ Weekly Comparison Dashboard

Smooth line chart showing who’s cruising and who’s struggling

Average trend line for a friendly competition vibe

Summary table with each user’s mean ease level

📊 All-Time Statistics

Total entries per user

Average ease levels

All-time trend chart with a soft aesthetic theme

Donut chart for “Easy” vs “Average” logs

🎨 Aesthetic UI

Creamy, clean theme (#FFF8E7 + warm browns)

Custom hover labels & smooth spline lines

“Made with Kakka by Saagar for Nikhil” footer 😎

🗓️ Smart Date Handling

Auto-cleans invalid dates from Google Sheet

Filters only the current week dynamically

🧩 Tech Stack
Component	Tech Used
Frontend	Streamlit

Visualization	Plotly

Data Source	Google Sheets API
Language	Python 3.x
Styling	Custom Plotly layout (cream aesthetic)
⚙️ Setup
1️⃣ Clone the repo
git clone https://github.com/yourusername/pooplog.git
cd pooplog

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Create .env file

Inside .env, add:

SHEET_URL="https://docs.google.com/spreadsheets/d/your_sheet_id_here"


(or however you connect to your Google Sheet — via st.secrets or gspread credentials)

4️⃣ Run Streamlit
streamlit run app.py


Then open your browser at http://localhost:8501 🚽

📅 How It Works

Each entry in the Google Sheet should look like this:

Date	User	Ease	Notes
2025-10-26	Me	0.9	Divine exit
2025-10-26	Nikhil	0.4	Slight turbulence

Ease: float between 0 (struggle 😖) and 1 (smooth 😌)

Notes: free text — poetic optional

🏆 Future Plans

🚀 Weekly Awards (“Smooth Operator”, “Constipation King”)
🧻 Poop Streak Tracker
📈 Gut Improvement Index
💬 Optional WhatsApp/Discord reminders
🌈 Dark Mode with animated toilet paper trails

🤝 Credits

Made with Kakka 🧻 by Saagar
 for Nikhil 💩
Because data means nothing… until it’s been properly flushed through Streamlit 🚽
