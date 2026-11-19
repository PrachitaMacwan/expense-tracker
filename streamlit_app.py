"""
streamlit_app.py - Web Interface for Personal Expense Tracker (Free Cloud Deployment)
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from database import DatabaseManager
from models import Transaction

# Page configuration
st.set_page_config(
    page_title="₹ Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
db = DatabaseManager("expenses.db")
db.seed_sample_data()

# Custom styles
st.markdown("""
<style>
    .metric-card {
        padding: 15px 20px;
        border-radius: 10px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

st.title("₹ Personal Expense & Budget Tracker")
st.caption("A simple, real-time personal finance manager built in Python.")

# --- Summary Statistics Cards ---
stats = db.get_summary()
inc = stats["total_income"]
exp = stats["total_expense"]
bal = stats["balance"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Income (Credits)", f"₹{inc:,.2f}")
with col2:
    st.metric("Total Expenses (Debits)", f"₹{exp:,.2f}")
with col3:
    st.metric("Net Balance (Savings)", f"₹{bal:,.2f}", delta=f"{bal:,.2f}")

st.divider()

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

# --- Sidebar: Add Transaction ---
with st.sidebar:
    st.header("➕ Add Transaction")
    with st.form("add_tx_form", clear_on_submit=True):
        t_type = st.radio("Type", ["Expense (खर्च)", "Income (आय)"], horizontal=True)
        resolved_type = "Expense" if "Expense" in t_type else "Income"

        amount = st.number_input("Amount (₹) *", min_value=1.0, step=50.0, format="%.2f")
        category = st.selectbox("Category *", CATEGORIES)
        t_date = st.date_input("Date *", value=datetime.today())
        desc = st.text_input("Note / Description")

        submitted = st.form_submit_button("💾 Save Record", use_container_width=True)
        if submitted:
            try:
                tx = Transaction(
                    trans_type=resolved_type,
                    amount=amount,
                    category=category,
                    date=t_date.strftime("%Y-%m-%d"),
                    description=desc
                )
                new_id = db.add_transaction(tx)
                st.success(f"Added record #{new_id} ({category} - ₹{amount:,.2f})!")
                st.rerun()
            except Exception as e:
                st.error(f"Error saving: {e}")

# --- Main Workspace: Tabs ---
tab1, tab2, tab3 = st.tabs(["📋 Transactions Table", "📊 Category Analytics", "📁 Export Data"])

with tab1:
    st.subheader("Transaction History")

    # Filters
    fcol1, fcol2, fcol3 = st.columns([1, 1, 2])
    with fcol1:
        f_type = st.selectbox("Filter Type", ["All", "Expense", "Income"])
    with fcol2:
        f_cat = st.selectbox("Filter Category", ["All"] + CATEGORIES)
    with fcol3:
        search_q = st.text_input("Search Description")

    records = db.filter_transactions(trans_type=f_type, category=f_cat, query=search_q)

    if records:
        df = pd.DataFrame([
            {
                "ID": r.id,
                "Date": r.date,
                "Type": r.trans_type,
                "Category": r.category,
                "Amount (₹)": r.amount,
                "Description": r.description
            } for r in records
        ])

        # Style table
        def color_type(val):
            return "color: #059669; font-weight: bold;" if val == "Income" else "color: #dc2626; font-weight: bold;"

        st.dataframe(
            df.style.map(color_type, subset=["Type"]).format({"Amount (₹)": "₹{:,.2f}"}),
            use_container_width=True,
            hide_index=True
        )

        # Delete single record
        st.divider()
        st.write("🗑️ **Delete a record:**")
        del_col1, del_col2 = st.columns([2, 1])
        record_labels = {r.id: f"ID #{r.id} - {r.category} (₹{r.amount:,.2f})" for r in records}
        with del_col1:
            record_to_del = st.selectbox(
                "Select Record to Delete",
                options=[r.id for r in records],
                format_func=lambda x: record_labels.get(x, str(x))
            )
        with del_col2:
            st.write("")
            st.write("")
            if st.button("Delete Record", type="secondary"):
                db.delete_transaction(record_to_del)
                st.warning(f"Record #{record_to_del} deleted.")
                st.rerun()
    else:
        st.info("No records found matching current filters.")

with tab2:
    st.subheader("Spending Breakdown by Category")
    breakdown = stats["category_breakdown"]
    if breakdown and exp > 0:
        b_df = pd.DataFrame(breakdown)
        b_df["Percentage"] = (b_df["total"] / exp) * 100
        b_df.columns = ["Category", "Total Spent (₹)", "Transactions Count", "Percentage (%)"]

        c_col1, c_col2 = st.columns([1, 1])
        with c_col1:
            st.dataframe(
                b_df.style.format({
                    "Total Spent (₹)": "₹{:,.2f}",
                    "Percentage (%)": "{:.1f}%"
                }),
                hide_index=True,
                use_container_width=True
            )
        with c_col2:
            chart_data = b_df.set_index("Category")["Total Spent (₹)"]
            st.bar_chart(chart_data)
    else:
        st.info("No expense data available for analytics yet.")

with tab3:
    st.subheader("Export Data to Spreadsheet")
    all_records = db.get_all_transactions()
    if all_records:
        export_df = pd.DataFrame([r.to_dict() for r in all_records])
        csv_data = export_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download All Transactions (CSV)",
            data=csv_data,
            file_name=f"expense_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        st.caption("This CSV file can be opened directly in Microsoft Excel or Google Sheets.")
    else:
        st.info("No data available to export.")
