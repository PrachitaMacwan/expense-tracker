"""
database.py - SQLite Database Manager for CRUD operations (INR / ₹)
"""
import sqlite3
import csv
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from models import Transaction


class DatabaseManager:
    """Manages SQLite database connections and CRUD operations."""

    def __init__(self, db_path: str = "expenses.db"):
        self.db_path = db_path
        self.init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Returns a configured SQLite connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """Creates tables and indexes if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trans_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON transactions(date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON transactions(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON transactions(trans_type)")
            conn.commit()

    def seed_sample_data(self) -> None:
        """Seeds realistic Indian Rupee (₹) initial transactions if the table is empty."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM transactions")
            if cursor.fetchone()[0] == 0:
                today = datetime.now()
                samples = [
                    ("Income", 45000.00, "Salary", today.strftime("%Y-%m-01"), "Monthly Salary Credit"),
                    ("Income", 6500.00, "Freelance / Side Income", (today - timedelta(days=10)).strftime("%Y-%m-%d"), "Client Website Design"),
                    ("Expense", 12000.00, "House Rent", today.strftime("%Y-%m-02"), "Monthly Apartment Rent"),
                    ("Expense", 4200.00, "Groceries / Ration", (today - timedelta(days=8)).strftime("%Y-%m-%d"), "Monthly Supermarket & Provisions"),
                    ("Expense", 1450.00, "Electricity & Bills", (today - timedelta(days=5)).strftime("%Y-%m-%d"), "Electricity & Water Bill"),
                    ("Expense", 1200.00, "Fuel & Travel", (today - timedelta(days=4)).strftime("%Y-%m-%d"), "Petrol & Metro Card Recharge"),
                    ("Expense", 750.00, "Food & Snacks", (today - timedelta(days=2)).strftime("%Y-%m-%d"), "Dinner with friends"),
                    ("Expense", 499.00, "Mobile & WiFi", today.strftime("%Y-%m-%d"), "Broadband Internet Recharge"),
                ]
                cursor.executemany("""
                    INSERT INTO transactions (trans_type, amount, category, date, description)
                    VALUES (?, ?, ?, ?, ?)
                """, samples)
                conn.commit()

    def add_transaction(self, tx: Transaction) -> int:
        """Inserts a new transaction into the database."""
        tx.validate()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (trans_type, amount, category, date, description)
                VALUES (?, ?, ?, ?, ?)
            """, (tx.trans_type, tx.amount, tx.category, tx.date, tx.description))
            conn.commit()
            tx.id = cursor.lastrowid
            return tx.id

    def update_transaction(self, tx: Transaction) -> bool:
        """Updates an existing transaction."""
        if tx.id is None:
            raise ValueError("Transaction ID cannot be None when updating.")
        tx.validate()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE transactions
                SET trans_type = ?, amount = ?, category = ?, date = ?, description = ?
                WHERE id = ?
            """, (tx.trans_type, tx.amount, tx.category, tx.date, tx.description, tx.id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_transaction(self, tx_id: int) -> bool:
        """Deletes a transaction by its primary key ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_transaction_by_id(self, tx_id: int) -> Optional[Transaction]:
        """Fetches a single transaction by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
            row = cursor.fetchone()
            if row:
                return Transaction(
                    id=row["id"],
                    trans_type=row["trans_type"],
                    amount=row["amount"],
                    category=row["category"],
                    date=row["date"],
                    description=row["description"] or ""
                )
        return None

    def get_all_transactions(self) -> List[Transaction]:
        """Returns all transactions sorted by date descending."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions ORDER BY date DESC, id DESC")
            rows = cursor.fetchall()
            return [
                Transaction(
                    id=r["id"],
                    trans_type=r["trans_type"],
                    amount=r["amount"],
                    category=r["category"],
                    date=r["date"],
                    description=r["description"] or ""
                ) for r in rows
            ]

    def filter_transactions(self, trans_type: Optional[str] = None,
                            category: Optional[str] = None,
                            query: Optional[str] = None,
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None) -> List[Transaction]:
        """Filters transactions based on type, category, keyword, and date range."""
        sql = "SELECT * FROM transactions WHERE 1=1"
        params: List[Any] = []

        if trans_type and trans_type != "All":
            sql += " AND trans_type = ?"
            params.append(trans_type)

        if category and category != "All":
            sql += " AND category = ?"
            params.append(category)

        if query and query.strip():
            sql += " AND (description LIKE ? OR category LIKE ?)"
            term = f"%{query.strip()}%"
            params.extend([term, term])

        if start_date and start_date.strip():
            sql += " AND date >= ?"
            params.append(start_date.strip())

        if end_date and end_date.strip():
            sql += " AND date <= ?"
            params.append(end_date.strip())

        sql += " ORDER BY date DESC, id DESC"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [
                Transaction(
                    id=r["id"],
                    trans_type=r["trans_type"],
                    amount=r["amount"],
                    category=r["category"],
                    date=r["date"],
                    description=r["description"] or ""
                ) for r in rows
            ]

    def get_summary(self) -> Dict[str, Any]:
        """Calculates total income, total expense, balance, and breakdown by category."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Total income
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE trans_type = 'Income'")
            total_income = cursor.fetchone()[0]

            # Total expenses
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE trans_type = 'Expense'")
            total_expense = cursor.fetchone()[0]

            # Category-wise expense breakdown
            cursor.execute("""
                SELECT category, COALESCE(SUM(amount), 0) as total, COUNT(*) as count
                FROM transactions
                WHERE trans_type = 'Expense'
                GROUP BY category
                ORDER BY total DESC
            """)
            category_breakdown = [
                {"category": r["category"], "total": r["total"], "count": r["count"]}
                for r in cursor.fetchall()
            ]

            return {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": total_income - total_expense,
                "category_breakdown": category_breakdown
            }

    def export_to_csv(self, file_path: str) -> int:
        """Exports all transactions to a CSV file. Returns the count of rows exported."""
        txs = self.get_all_transactions()
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Type", "Amount (INR)", "Category", "Date", "Description"])
            for t in txs:
                writer.writerow([t.id, t.trans_type, f"{t.amount:.2f}", t.category, t.date, t.description])
        return len(txs)
