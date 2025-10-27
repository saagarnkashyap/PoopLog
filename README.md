# 💩 PoopLog – The Weekly Ease Tracker

> “Because every smooth journey deserves recognition.”  
> **Track. Compare. Reflect. 💩**

---

## 🧠 Overview

**PoopLog** is a Streamlit-based web app designed for *ultimate bowel accountability between friends.*  
It syncs data from a shared Google Sheet, turning daily dumps into delightful data visualizations.

It’s part science, part fun — and entirely serious about gut progress.  
Watch your ease scores evolve through clean plots, summaries, and weekly leaderboards!

---

## ✨ Features

### ✅ Weekly Comparison Dashboard
- Smooth line chart showing who’s cruising and who’s struggling  
- Average trend line for a friendly competition vibe  
- Summary table with each user’s mean ease level  

### 📊 All-Time Statistics
- Total entries per user  
- Average ease levels  
- All-time trend chart with a soft aesthetic theme  
- Donut chart for “Easy” vs “Average” logs  

### 🎨 Aesthetic UI
- Creamy, clean theme (`#FFF8E7` + warm browns)  
- Custom hover labels & smooth spline lines  
- “*Made with Kakka by Saagar for Nikhil*” footer 😎  

### 🗓️ Smart Date Handling
- Auto-cleans invalid dates from Google Sheet  
- Filters only the *current week* dynamically  

---

## 🧩 Tech Stack

| Component | Tech Used |
|------------|-----------|
| Frontend | Streamlit |
| Visualization | Plotly |
| Data Source | Google Sheets API |
| Language | Python 3.x |
| Styling | Custom Plotly layout (cream aesthetic) |

---

## ⚙️ Setup & Run Instructions

### 🧰 Step 1: Clone the Repo
```bash
git clone https://github.com/yourusername/pooplog.git
cd pooplog
```

### 🧩 Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### 🧾 Step 3: Create `.env` File
Inside your project folder, create a file named `.env` and add your Google Sheet link:

```bash
SHEET_URL="https://docs.google.com/spreadsheets/d/your_sheet_id_here"
```

If you’re using a private sheet (not public CSV link), configure your credentials instead via:
```bash
mkdir .streamlit
nano .streamlit/secrets.toml
```

Then paste:
```toml
[gcp_service_account]
type = "service_account"
project_id = "your_project_id"
private_key_id = "your_private_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"
client_email = "your_email@project.iam.gserviceaccount.com"
client_id = "your_client_id"
```

---

### 🚀 Step 4: Run Streamlit
```bash
streamlit run app.py
```

Then open your browser at  
👉 [http://localhost:8501](http://localhost:8501)

---

## 📅 How It Works

Each entry in your Google Sheet should look like this:

| Date | User | Ease | Notes |
|------|------|------|-------|
| 2025-10-26 | Me | 0.9 | Divine exit |
| 2025-10-26 | Nikhil | 0.4 | Slight turbulence |

- **Date:** `YYYY-MM-DD`  
- **Ease:** Float between `0` (😖 struggle) and `1` (😌 smooth)  
- **Notes:** Optional — poetic freedom encouraged  

Your PoopLog app automatically:
1. Fetches the latest sheet data  
2. Cleans invalid or empty entries  
3. Filters the current week dynamically  
4. Displays weekly summaries, averages, and all-time stats  

---

## 🏆 Future Plans

- 🚀 **Weekly Awards:** “Smooth Operator”, “Constipation King”  
- 🧻 **Poop Streak Tracker:** daily consistency visual  
- 📈 **Gut Improvement Index:** week-over-week health metric  
- 💬 **Reminders:** optional WhatsApp/Discord logs  
- 🌈 **Dark Mode:** animated toilet paper trails & glow UI  

---

## 🤝 Credits

Made with **Kakka 🧻 by Saagar**  
for **Nikhil 💩**

Because data means nothing…  
until it’s been properly flushed through Streamlit 🚽
