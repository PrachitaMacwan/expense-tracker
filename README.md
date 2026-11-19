# ₹ Personal Expense & Budget Tracker (INR)

A clean, modern personal finance manager built in Python with SQLite.
Available both as a **Desktop GUI Application** (Tkinter) and a **Live Web Application** (Streamlit).

---

## 📌 Project Overview

- **Subject / Level**: Python Programming (Mini Project)
- **Currency**: **Indian Rupee (₹ INR)**
- **Architecture**: Modular OOP Design (Separation of Data Models, Database, and UI)
- **Database**: SQLite3 (`expenses.db` embedded relational database)
- **Interfaces**:
  - **Desktop GUI**: Python Tkinter with `ttk` (Runs natively on Windows/macOS/Linux)
  - **Web Application**: Streamlit (Deployable live to the web for free)

---

## 📁 Project Structure

```text
expense_tracker/
├── main.py            # Desktop app entry point (Tkinter GUI)
├── streamlit_app.py   # Web app entry point (Streamlit - for live deployment)
├── models.py          # OOP Data Models and input validation
├── database.py        # SQLite Database Manager and CRUD operations in ₹
├── gui.py             # Desktop Tkinter GUI window and event handling
├── requirements.txt   # Web dependencies (streamlit, pandas)
├── .gitignore         # Ignores temp files and caches for clean Git commits
├── expenses.db        # SQLite database (auto-created on first run)
└── README.md          # Complete documentation & Viva preparation
```

---

## 🚀 How to Run Locally

### Option 1: Desktop Application (Tkinter)
Zero external libraries needed — works immediately with standard Python:
```bash
python main.py
```

### Option 2: Web Application (Streamlit)
To run the browser version locally:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 🌐 How to Deploy Live Publicly (Free Web Link)

You can get a free, permanent link (e.g. `https://my-expense-tracker.streamlit.app`) to share with teachers, friends, or on your resume:

1. **Push your code to GitHub** (follow the steps below).
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in with your GitHub account.
3. Click **"New app"**.
4. Select your GitHub repository (`expense_tracker`).
5. Set Main file path to: `streamlit_app.py`.
6. Click **"Deploy!"**.
7. In about 1–2 minutes, your project will be live with a public URL that anyone can open on a phone or laptop!

---

## 🐙 How to Upload to GitHub

### Method A: Direct Upload via Web Browser (Easiest — No Git required)
1. Go to [github.com](https://github.com/) and log in (or sign up).
2. Click the **"+"** icon in the top right and select **New repository**.
3. Name it `expense-tracker` and set it to **Public**. Leave "Add a README file" unchecked (since we already have one). Click **Create repository**.
4. On the next page, click the link: **"uploading an existing file"**.
5. Drag and drop all the files from your folder:
   - `main.py`
   - `gui.py`
   - `models.py`
   - `database.py`
   - `streamlit_app.py`
   - `requirements.txt`
   - `.gitignore`
   - `README.md`
6. Click **Commit changes**. Your project is now live on GitHub!

---

### Method B: Using Git Command Line
If you have Git installed (or install it via `winget install Git.Git`):
```bash
cd "C:\Users\Hp15s-2144AU\.gemini\antigravity\scratch\expense_tracker"
git init
git add .
git commit -m "Initial commit: Personal Expense Tracker in INR"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/expense-tracker.git
git push -u origin main
```

---

## 📦 How to Create a Standalone Windows Executable (.exe)

Want anyone to double-click and run the Desktop app without needing Python installed?

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the `.exe`:
   ```bash
   pyinstaller --onefile --noconsole --name="ExpenseTracker" main.py
   ```
3. Your standalone executable will be in the `dist/` folder (`ExpenseTracker.exe`).
4. You can attach this `.exe` file to your **GitHub Releases** page!
