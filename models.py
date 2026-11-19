"""
models.py - Transaction Data Model with OOP and Validation
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    """Represents a single financial transaction (Income or Expense)."""
    id: Optional[int] = None
    trans_type: str = "Expense"  # 'Expense' or 'Income'
    amount: float = 0.0
    category: str = "General"
    date: str = ""               # Formatted as YYYY-MM-DD
    description: str = ""

    def validate(self) -> None:
        """Validates the transaction fields. Raises ValueError if invalid."""
        if self.trans_type not in ("Income", "Expense"):
            raise ValueError("Transaction type must be 'Income' or 'Expense'.")

        try:
            val = float(self.amount)
            if val <= 0:
                raise ValueError("Amount must be greater than zero.")
            self.amount = round(val, 2)
        except (TypeError, ValueError) as err:
            raise ValueError(f"Invalid amount: {err}")

        if not self.category or not self.category.strip():
            raise ValueError("Category cannot be empty.")
        self.category = self.category.strip()

        if not self.date or not self.date.strip():
            raise ValueError("Date cannot be empty.")
        try:
            # Validate standard YYYY-MM-DD format
            datetime.strptime(self.date.strip(), "%Y-%m-%d")
            self.date = self.date.strip()
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format (e.g. 2026-11-20).")

        self.description = self.description.strip() if self.description else ""

    def to_dict(self) -> dict:
        """Converts model to dictionary."""
        return {
            "id": self.id,
            "type": self.trans_type,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }
