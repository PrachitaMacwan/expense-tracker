"""
main.py - Entry Point for Personal Expense & Budget Tracker
"""
import sys
import tkinter as tk
from database import DatabaseManager
from gui import ExpenseTrackerGUI


def main():
    # 1. Initialize SQLite Database
    db = DatabaseManager("expenses.db")

    # 2. Populate sample records if first run (for presentation/evaluation readiness)
    db.seed_sample_data()

    # 3. Initialize Tkinter Desktop Window
    root = tk.Tk()

    # Set icon/title properties if needed
    try:
        # Graceful handling if on standard desktop
        root.state("normal")
    except Exception:
        pass

    app = ExpenseTrackerGUI(root, db)

    # 4. Start Event Loop
    root.mainloop()


if __name__ == "__main__":
    main()
