"""
gui.py - Simple & Intuitive Tkinter GUI for Personal Expense Tracker (INR / ₹)
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Optional
from models import Transaction
from database import DatabaseManager


class ExpenseTrackerGUI:
    """Main Application GUI window."""

    CATEGORIES = [
        "Food & Dining",
        "Groceries / Ration",
        "House Rent",
        "Electricity & Bills",
        "Fuel & Travel",
        "Mobile & WiFi",
        "Shopping",
        "Medical & Health",
        "Education & College Fees",
        "Entertainment & Movies",
        "Salary",
        "Freelance / Side Income",
        "Other"
    ]

    def __init__(self, root: tk.Tk, db: DatabaseManager):
        self.root = root
        self.db = db
        self.selected_tx_id: Optional[int] = None

        self.root.title("Personal Expense & Budget Tracker (₹ INR)")
        self.root.geometry("1120x720")
        self.root.minsize(1000, 640)

        # Configure style
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self._configure_styles()
        self._build_ui()
        self.refresh_all()

    def _configure_styles(self) -> None:
        """Configures clean fonts, pleasant colors, and ttk element styles."""
        bg_main = "#f8fafc"
        self.root.configure(bg=bg_main)

        # Treeview styling
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#e2e8f0",
            foreground="#1e293b",
            relief="flat",
            padding=7
        )
        self.style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=30,
            background="#ffffff",
            fieldbackground="#ffffff"
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#3b82f6")],
            foreground=[("selected", "#ffffff")]
        )

        self.style.configure("TCombobox", padding=4)
        self.style.configure("TEntry", padding=4)

    def _build_ui(self) -> None:
        """Constructs layout: Top Header -> Summary Cards -> Main Split (Form + Table) -> Status Bar."""
        # --- Top Header ---
        header_frame = tk.Frame(self.root, bg="#0f172a", height=65)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_lbl = tk.Label(
            header_frame,
            text="₹ Expense & Budget Tracker",
            font=("Segoe UI", 16, "bold"),
            bg="#0f172a",
            fg="#f8fafc"
        )
        title_lbl.pack(side=tk.LEFT, padx=25, pady=16)

        subtitle_lbl = tk.Label(
            header_frame,
            text="Simple Daily Finance Manager (INR)",
            font=("Segoe UI", 10),
            bg="#0f172a",
            fg="#94a3b8"
        )
        subtitle_lbl.pack(side=tk.RIGHT, padx=25, pady=20)

        # --- Dashboard Summary Cards (Income / Expense / Balance) ---
        self.cards_frame = tk.Frame(self.root, bg="#f8fafc", pady=12, padx=20)
        self.cards_frame.pack(fill=tk.X)

        self.card_income = self._create_card(self.cards_frame, "Total Income (Credits)", "₹0.00", "#059669", "#ecfdf5", "#a7f3d0")
        self.card_expense = self._create_card(self.cards_frame, "Total Expenses (Debits)", "₹0.00", "#dc2626", "#fef2f2", "#fecaca")
        self.card_balance = self._create_card(self.cards_frame, "Net Balance (Savings)", "₹0.00", "#2563eb", "#eff6ff", "#bfdbfe")

        self.card_income["frame"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)
        self.card_expense["frame"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)
        self.card_balance["frame"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)

        # --- Main Workspace Split ---
        content_frame = tk.Frame(self.root, bg="#f8fafc", padx=20, pady=6)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left Column: Easy Input Form (Width ~340px)
        form_outer = tk.Frame(content_frame, bg="#ffffff", bd=1, relief=tk.SOLID, padx=18, pady=16)
        form_outer.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        self._build_form(form_outer)

        # Right Column: Filter Bar + Table + Bottom Controls
        table_outer = tk.Frame(content_frame, bg="#ffffff", bd=1, relief=tk.SOLID, padx=15, pady=14)
        table_outer.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self._build_table_section(table_outer)

        # --- Bottom Status Bar ---
        self.status_bar = tk.Label(
            self.root,
            text="Ready. Select any row to view, edit, or delete.",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#64748b",
            anchor=tk.W,
            padx=20,
            pady=4
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _create_card(self, parent: tk.Widget, title: str, default_val: str, text_color: str, bg_color: str, border_color: str) -> dict:
        """Creates clean, modern metric cards."""
        card = tk.Frame(parent, bg=bg_color, highlightbackground=border_color, highlightthickness=1, padx=16, pady=12)
        title_lbl = tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), fg="#64748b", bg=bg_color)
        title_lbl.pack(anchor=tk.W)

        val_lbl = tk.Label(card, text=default_val, font=("Segoe UI", 18, "bold"), fg=text_color, bg=bg_color)
        val_lbl.pack(anchor=tk.W, pady=(4, 0))

        return {"frame": card, "val_lbl": val_lbl}

    def _build_form(self, container: tk.Widget) -> None:
        """Builds clean, easy-to-use input form."""
        self.form_title = tk.Label(
            container,
            text="➕ Add New Transaction",
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff",
            fg="#0f172a"
        )
        self.form_title.pack(anchor=tk.W, pady=(0, 12))

        # 1. Type selector (Expense / Income)
        tk.Label(container, text="Type:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#334155").pack(anchor=tk.W)
        self.var_type = tk.StringVar(value="Expense")
        type_frame = tk.Frame(container, bg="#ffffff")
        type_frame.pack(fill=tk.X, pady=(2, 10))

        rb_expense = tk.Radiobutton(
            type_frame, text="Expense (खर्च)", variable=self.var_type, value="Expense",
            bg="#ffffff", activebackground="#ffffff", font=("Segoe UI", 9, "bold"), fg="#dc2626", selectcolor="#ffffff"
        )
        rb_expense.pack(side=tk.LEFT, padx=(0, 15))

        rb_income = tk.Radiobutton(
            type_frame, text="Income (आय)", variable=self.var_type, value="Income",
            bg="#ffffff", activebackground="#ffffff", font=("Segoe UI", 9, "bold"), fg="#059669", selectcolor="#ffffff"
        )
        rb_income.pack(side=tk.LEFT)

        # 2. Amount in Rupee (₹)
        tk.Label(container, text="Amount (₹) *:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#334155").pack(anchor=tk.W)
        self.var_amount = tk.StringVar()
        self.ent_amount = ttk.Entry(container, textvariable=self.var_amount, font=("Segoe UI", 11))
        self.ent_amount.pack(fill=tk.X, pady=(2, 10))
        self.ent_amount.bind("<Return>", lambda e: self.save_transaction())

        # 3. Category
        tk.Label(container, text="Category *:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#334155").pack(anchor=tk.W)
        self.var_category = tk.StringVar(value="Food & Dining")
        self.combo_category = ttk.Combobox(container, textvariable=self.var_category, values=self.CATEGORIES, state="readonly", font=("Segoe UI", 9))
        self.combo_category.pack(fill=tk.X, pady=(2, 10))

        # 4. Date (with quick 'Today' button)
        tk.Label(container, text="Date (YYYY-MM-DD) *:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#334155").pack(anchor=tk.W)
        date_frame = tk.Frame(container, bg="#ffffff")
        date_frame.pack(fill=tk.X, pady=(2, 10))

        self.var_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.ent_date = ttk.Entry(date_frame, textvariable=self.var_date, font=("Segoe UI", 9))
        self.ent_date.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_today = tk.Button(
            date_frame,
            text="Today",
            font=("Segoe UI", 8),
            bg="#e2e8f0",
            fg="#1e293b",
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            command=self.set_today_date
        )
        btn_today.pack(side=tk.RIGHT, padx=(4, 0))

        # 5. Description / Notes
        tk.Label(container, text="Note / Description:", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#334155").pack(anchor=tk.W)
        self.var_desc = tk.StringVar()
        self.ent_desc = ttk.Entry(container, textvariable=self.var_desc, font=("Segoe UI", 9))
        self.ent_desc.pack(fill=tk.X, pady=(2, 14))
        self.ent_desc.bind("<Return>", lambda e: self.save_transaction())

        # 6. Action Buttons
        self.btn_save = tk.Button(
            container,
            text="💾 Save Record",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            pady=7,
            command=self.save_transaction
        )
        self.btn_save.pack(fill=tk.X, pady=(0, 6))

        self.btn_clear = tk.Button(
            container,
            text="🔄 Clear / Reset",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#475569",
            relief=tk.FLAT,
            cursor="hand2",
            pady=4,
            command=self.clear_form
        )
        self.btn_clear.pack(fill=tk.X, pady=(0, 12))

        # Tools separator
        sep = ttk.Separator(container, orient="horizontal")
        sep.pack(fill=tk.X, pady=6)

        tk.Label(container, text="Reports & Tools:", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#94a3b8").pack(anchor=tk.W, pady=(2, 6))

        # Category Breakdown Report button
        btn_analytics = tk.Button(
            container,
            text="📊 Category Spending Report",
            font=("Segoe UI", 9),
            bg="#f8fafc",
            fg="#0f172a",
            relief=tk.GROOVE,
            cursor="hand2",
            pady=4,
            command=self.show_analytics_dialog
        )
        btn_analytics.pack(fill=tk.X, pady=(0, 6))

        # CSV Export button
        btn_export = tk.Button(
            container,
            text="📁 Export to Excel / CSV",
            font=("Segoe UI", 9),
            bg="#f8fafc",
            fg="#0f172a",
            relief=tk.GROOVE,
            cursor="hand2",
            pady=4,
            command=self.export_csv
        )
        btn_export.pack(fill=tk.X)

    def _build_table_section(self, container: tk.Widget) -> None:
        """Builds search filter bar, transactions table, and deletion action."""
        # --- Top Filter & Search Bar ---
        filter_bar = tk.Frame(container, bg="#ffffff")
        filter_bar.pack(fill=tk.X, pady=(0, 10))

        # Type filter
        tk.Label(filter_bar, text="Type:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 4))
        self.filter_type_var = tk.StringVar(value="All")
        combo_ftype = ttk.Combobox(filter_bar, textvariable=self.filter_type_var, values=["All", "Expense", "Income"], width=9, state="readonly")
        combo_ftype.pack(side=tk.LEFT, padx=(0, 10))
        combo_ftype.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())

        # Category filter
        tk.Label(filter_bar, text="Category:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 4))
        self.filter_cat_var = tk.StringVar(value="All")
        combo_fcat = ttk.Combobox(filter_bar, textvariable=self.filter_cat_var, values=["All"] + self.CATEGORIES, width=15, state="readonly")
        combo_fcat.pack(side=tk.LEFT, padx=(0, 10))
        combo_fcat.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())

        # Search Query
        tk.Label(filter_bar, text="Search:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 4))
        self.search_var = tk.StringVar()
        ent_search = ttk.Entry(filter_bar, textvariable=self.search_var, width=14)
        ent_search.pack(side=tk.LEFT, padx=(0, 6))
        ent_search.bind("<Return>", lambda e: self.apply_filter())

        btn_search = tk.Button(
            filter_bar,
            text="Filter",
            font=("Segoe UI", 8, "bold"),
            bg="#e2e8f0",
            relief=tk.FLAT,
            padx=8,
            cursor="hand2",
            command=self.apply_filter
        )
        btn_search.pack(side=tk.LEFT, padx=(0, 4))

        btn_reset = tk.Button(
            filter_bar,
            text="Reset",
            font=("Segoe UI", 8),
            bg="#f1f5f9",
            relief=tk.FLAT,
            padx=8,
            cursor="hand2",
            command=self.reset_filter
        )
        btn_reset.pack(side=tk.LEFT)

        # --- Table (Treeview) ---
        table_container = tk.Frame(container, bg="#ffffff")
        table_container.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "date", "type", "category", "amount", "description")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount (₹)")
        self.tree.heading("description", text="Description / Note")

        self.tree.column("id", width=45, anchor=tk.CENTER)
        self.tree.column("date", width=95, anchor=tk.CENTER)
        self.tree.column("type", width=80, anchor=tk.CENTER)
        self.tree.column("category", width=145, anchor=tk.W)
        self.tree.column("amount", width=115, anchor=tk.E)
        self.tree.column("description", width=230, anchor=tk.W)

        # Tag styles for colors: Green for Income, Red for Expense
        self.tree.tag_configure("income_row", foreground="#059669")
        self.tree.tag_configure("expense_row", foreground="#dc2626")

        vsb = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        # --- Table Footer ---
        footer_bar = tk.Frame(container, bg="#ffffff", pady=8)
        footer_bar.pack(fill=tk.X)

        self.lbl_record_count = tk.Label(
            footer_bar,
            text="Showing 0 record(s)  •  💡 Click any record to edit or delete",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#64748b"
        )
        self.lbl_record_count.pack(side=tk.LEFT)

        btn_delete = tk.Button(
            footer_bar,
            text="🗑️ Delete Selected Record",
            font=("Segoe UI", 9, "bold"),
            bg="#fee2e2",
            fg="#b91c1c",
            activebackground="#fca5a5",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.delete_selected
        )
        btn_delete.pack(side=tk.RIGHT)

    # --- Core Functionality ---

    def set_today_date(self) -> None:
        """Sets date field to current system date."""
        self.var_date.set(datetime.now().strftime("%Y-%m-%d"))

    def refresh_all(self) -> None:
        """Refreshes summary statistics cards and table."""
        self.refresh_summary()
        self.apply_filter()

    def refresh_summary(self) -> None:
        """Updates metric cards in Indian Rupees (₹)."""
        stats = self.db.get_summary()
        inc = stats["total_income"]
        exp = stats["total_expense"]
        bal = stats["balance"]

        self.card_income["val_lbl"].config(text=f"₹{inc:,.2f}")
        self.card_expense["val_lbl"].config(text=f"₹{exp:,.2f}")

        bal_str = f"₹{bal:,.2f}" if bal >= 0 else f"-₹{abs(bal):,.2f}"
        self.card_balance["val_lbl"].config(
            text=bal_str,
            fg="#059669" if bal >= 0 else "#dc2626"
        )

    def load_transactions_to_table(self, transactions) -> None:
        """Populates Treeview with transactions in ₹."""
        self.tree.delete(*self.tree.get_children())
        for tx in transactions:
            tag = "income_row" if tx.trans_type == "Income" else "expense_row"
            sign = "+" if tx.trans_type == "Income" else "-"
            amt_display = f"{sign}₹{tx.amount:,.2f}"
            self.tree.insert(
                "",
                tk.END,
                values=(tx.id, tx.date, tx.trans_type, tx.category, amt_display, tx.description),
                tags=(tag,)
            )
        self.lbl_record_count.config(text=f"Showing {len(transactions)} record(s)  •  💡 Click any record to edit or delete")

    def apply_filter(self) -> None:
        """Applies filter selections to database query."""
        ftype = self.filter_type_var.get()
        fcat = self.filter_cat_var.get()
        q = self.search_var.get()
        results = self.db.filter_transactions(trans_type=ftype, category=fcat, query=q)
        self.load_transactions_to_table(results)

    def reset_filter(self) -> None:
        """Clears all filters and reloads all records."""
        self.filter_type_var.set("All")
        self.filter_cat_var.set("All")
        self.search_var.set("")
        self.apply_filter()
        self.set_status("Filter reset. Showing all transactions.")

    def on_row_selected(self, event=None) -> None:
        """Fills form when user selects a row for editing."""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = self.tree.item(selected_items[0])
        vals = item["values"]
        if not vals:
            return

        self.selected_tx_id = int(vals[0])
        tx = self.db.get_transaction_by_id(self.selected_tx_id)
        if tx:
            self.var_type.set(tx.trans_type)
            self.var_amount.set(f"{tx.amount:.2f}".rstrip("0").rstrip(".") if tx.amount.is_integer() else str(tx.amount))
            self.var_category.set(tx.category)
            self.var_date.set(tx.date)
            self.var_desc.set(tx.description)

            self.form_title.config(text=f"✏️ Edit Record #{tx.id}", fg="#2563eb")
            self.btn_save.config(text="✅ Update Record", bg="#0d9488")
            self.set_status(f"Editing Transaction #{tx.id}. Make changes and click 'Update Record'.")

    def clear_form(self) -> None:
        """Clears the input form back to fresh state."""
        self.selected_tx_id = None
        self.var_type.set("Expense")
        self.var_amount.set("")
        self.var_category.set("Food & Dining")
        self.set_today_date()
        self.var_desc.set("")

        self.form_title.config(text="➕ Add New Transaction", fg="#0f172a")
        self.btn_save.config(text="💾 Save Record", bg="#2563eb")

        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

        self.set_status("Ready to add a new transaction.")

    def save_transaction(self) -> None:
        """Handles saving (Create or Update)."""
        trans_type = self.var_type.get()
        amount_str = self.var_amount.get().strip()
        category = self.var_category.get().strip()
        date_str = self.var_date.get().strip()
        desc = self.var_desc.get().strip()

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid numeric amount in ₹ (e.g., 500 or 1250.50).")
            self.ent_amount.focus_set()
            return

        tx = Transaction(
            id=self.selected_tx_id,
            trans_type=trans_type,
            amount=amount,
            category=category,
            date=date_str,
            description=desc
        )

        try:
            tx.validate()
        except ValueError as err:
            messagebox.showerror("Validation Error", str(err))
            return

        try:
            if self.selected_tx_id is None:
                # Add new record
                new_id = self.db.add_transaction(tx)
                self.set_status(f"Success! Added new record #{new_id} ({category} - ₹{amount:,.2f})")
                messagebox.showinfo("Saved", f"Transaction #{new_id} of ₹{amount:,.2f} added successfully!")
            else:
                # Update existing record
                self.db.update_transaction(tx)
                self.set_status(f"Success! Updated record #{tx.id}")
                messagebox.showinfo("Updated", f"Transaction #{tx.id} updated successfully!")

            self.clear_form()
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save record: {e}")

    def delete_selected(self) -> None:
        """Deletes selected transaction after user confirmation."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Select a Record", "Please click on a record in the table first to select it.")
            return

        item = self.tree.item(selected_items[0])
        tx_id = int(item["values"][0])
        category = item["values"][3]
        amt = item["values"][4]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this transaction?\n\nRecord ID: #{tx_id}\nCategory: {category}\nAmount: {amt}"
        )
        if confirm:
            self.db.delete_transaction(tx_id)
            self.clear_form()
            self.refresh_all()
            self.set_status(f"Record #{tx_id} was successfully deleted.")
            messagebox.showinfo("Deleted", "Transaction deleted successfully.")

    def export_csv(self) -> None:
        """Exports data to a CSV spreadsheet."""
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Spreadsheet", "*.csv"), ("All files", "*.*")],
            initialfile=f"expense_report_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        if path:
            count = self.db.export_to_csv(path)
            self.set_status(f"Exported {count} records to {path}")
            messagebox.showinfo("Export Successful", f"Successfully exported {count} records to:\n\n{path}")

    def show_analytics_dialog(self) -> None:
        """Opens clean spending breakdown report in ₹ with visual indicators."""
        stats = self.db.get_summary()
        breakdown = stats["category_breakdown"]
        total_exp = stats["total_expense"]

        win = tk.Toplevel(self.root)
        win.title("Expense Spending Breakdown (₹ INR)")
        win.geometry("540x480")
        win.minsize(480, 400)
        win.transient(self.root)
        win.grab_set()

        header_frame = tk.Frame(win, bg="#fef2f2", pady=12)
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text=f"Total Expenses: ₹{total_exp:,.2f}",
            font=("Segoe UI", 13, "bold"),
            fg="#b91c1c",
            bg="#fef2f2"
        ).pack()

        if not breakdown or total_exp <= 0:
            tk.Label(win, text="No expense records available yet.", pady=40, font=("Segoe UI", 10), fg="#64748b").pack()
            return

        body = tk.Frame(win, padx=20, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        for item in breakdown:
            cat = item["category"]
            tot = item["total"]
            pct = (tot / total_exp) * 100

            row = tk.Frame(body, pady=5)
            row.pack(fill=tk.X)

            # Category & %
            lbl_cat = tk.Label(row, text=f"{cat} ({pct:.1f}%)", font=("Segoe UI", 9, "bold"), width=22, anchor=tk.W)
            lbl_cat.pack(side=tk.LEFT)

            # Bar indicator
            bar_bg = tk.Frame(row, bg="#e2e8f0", height=14, width=150)
            bar_bg.pack(side=tk.LEFT, padx=6)
            bar_bg.pack_propagate(False)

            fill_w = max(2, int((pct / 100) * 150))
            bar_fill = tk.Frame(bar_bg, bg="#ef4444", width=fill_w, height=14)
            bar_fill.pack(side=tk.LEFT)

            # Amount in ₹
            lbl_amt = tk.Label(row, text=f"₹{tot:,.2f}", font=("Segoe UI", 9), anchor=tk.E, width=14)
            lbl_amt.pack(side=tk.RIGHT)

        btn_close = ttk.Button(win, text="Close Report", command=win.destroy)
        btn_close.pack(pady=15)

    def set_status(self, message: str) -> None:
        """Updates bottom status bar text."""
        self.status_bar.config(text=f"📌 {message}")
