# main.py - Swordigo-themed Streamlit ATM Dashboard (one action per login)

import streamlit as st
from storage import load_accounts, load_cash, load_reports, save_accounts, accounts
from account_module import withdraw, deposit, current_balance, transfer_funds
from admin_module import admin_add_cash, view_cash, view_reports
from datetime import datetime

# ----------------------------
# INITIAL LOAD
# ----------------------------
load_accounts()
load_cash()
load_reports()

st.set_page_config(page_title="Swordigo ATM", page_icon="⚔️", layout="wide")

# Initialize session state
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None
if "action_selected" not in st.session_state:
    st.session_state["action_selected"] = None
if "action_done" not in st.session_state:
    st.session_state["action_done"] = None
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# ----------------------------
# CSS Styling
# ----------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1e2a78, #4a60b0);
    color: #eef2ff;
}
.big-button .stButton>button {
    background: linear-gradient(90deg,#3b4cca,#6b86ff);
    color: white;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 700;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}
.card {
    background: rgba(255,255,255,0.03);
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
st.title("⚔️ Swordigo ATM Dashboard")
st.write("Welcome — use the sidebar to navigate. Users can perform **one action per login**; click Logout to end session.")

side = st.sidebar
page = side.radio("Menu", ["Home", "Login", "Register", "Admin", "Reports"])

# ----------------------------
# HOME PAGE (Simplified)
# ----------------------------
if page == "Home":
    st.header("ATM Overview")
    st.write("Welcome to ⚔️ Swordigo ATM. Use the sidebar to navigate to Login, Register, Admin, or Reports.")

# ----------------------------
# REGISTER PAGE
# ----------------------------
elif page == "Register":
    st.header("Create New Account")
    acc_no = st.text_input("Account Number", key="reg_acc")
    name = st.text_input("Name", key="reg_name")
    pin = st.text_input("4-digit PIN", key="reg_pin", type="password")
    init = st.number_input("Initial Deposit", min_value=0.0, key="reg_init")
    if st.button("Register"):
        if not acc_no or not pin or len(pin) != 4:
            st.error("Provide valid account number and 4-digit PIN.")
        elif acc_no in accounts:
            st.error("Account already exists.")
        else:
            accounts[acc_no] = {"name": name, "pin": pin, "balance": float(init), "active": True}
            save_accounts()
            st.success(f"✅ Account {acc_no} created for {name}.")

# ----------------------------
# USER LOGIN PAGE (one action per login)
# ----------------------------
elif page == "Login":
    st.header("🔐 User Login")

    # Show logout / info if already logged in
    if st.session_state["logged_in_user"]:
        acc = st.session_state["logged_in_user"]
        st.success(f"Logged in as: {accounts[acc]['name']} (Account: {acc})")
        if st.session_state.get("action_done") is None:
            st.info("You can perform **one action** only per login.")
        if st.button("Logout"):
            st.session_state["logged_in_user"] = None
            st.session_state["action_selected"] = None
            st.session_state["action_done"] = None
            st.info("You have been logged out.")
    else:
        acc_no = st.text_input("Account Number", key="login_acc")
        pin = st.text_input("PIN", key="login_pin", type="password")
        if st.button("Login"):
            if acc_no in accounts and accounts[acc_no]["pin"] == pin:
                if not accounts[acc_no]["active"]:
                    st.error("🚫 Account is deactivated.")
                else:
                    st.session_state["logged_in_user"] = acc_no
                    st.session_state["action_selected"] = None
                    st.session_state["action_done"] = None
                    st.success(f"✅ Welcome {accounts[acc_no]['name']} — choose **one action** below.")
            else:
                st.error("❌ Invalid credentials.")

    # Actions (only if user is logged in and hasn't done an action)
    if st.session_state["logged_in_user"] and st.session_state.get("action_done") is None:
        c1, c2, c3, c4 = st.columns(4)

        # Withdraw
        with c1:
            if st.button("🏧 Withdraw", key="btn_withdraw"):
                st.session_state["action_selected"] = "withdraw"
        if st.session_state["action_selected"] == "withdraw":
            amt = st.number_input("Amount to withdraw", min_value=0, step=100, key="withdraw_amt")
            if st.button("Confirm Withdraw", key="confirm_withdraw"):
                res = withdraw(acc, int(amt))
                st.info(res)
                st.session_state["action_done"] = True
                st.success("Action complete. Please logout to perform another action.")

        # Deposit
        with c2:
            if st.button("💰 Deposit", key="btn_deposit"):
                st.session_state["action_selected"] = "deposit"
        if st.session_state["action_selected"] == "deposit":
            damt = st.number_input("Amount to deposit", min_value=0.0, step=100.0, key="deposit_amt")
            if st.button("Confirm Deposit", key="confirm_deposit"):
                res = deposit(acc, float(damt))
                st.info(res)
                st.session_state["action_done"] = True
                st.success("Action complete. Please logout to perform another action.")

        # Check Balance
        with c3:
            if st.button("📄 Check Balance", key="btn_balance"):
                res = current_balance(acc)
                st.info(res)
                st.session_state["action_done"] = True
                st.success("Action complete. Please logout to perform another action.")

        # Transfer
        with c4:
            if st.button("🔁 Transfer", key="btn_transfer"):
                st.session_state["action_selected"] = "transfer"
        if st.session_state["action_selected"] == "transfer":
            recv = st.text_input("Receiver Account No.", key="transfer_recv")
            tamt = st.number_input("Amount", min_value=0.0, step=100.0, key="transfer_amt")
            if st.button("Confirm Transfer", key="confirm_transfer"):
                res = transfer_funds(acc, recv, float(tamt))
                st.info(res)
                st.session_state["action_done"] = True
                st.success("Action complete. Please logout to perform another action.")

# ----------------------------
# ADMIN PANEL
# ----------------------------
elif page == "Admin":
    st.header("👨‍💼 Admin Panel — Manage Cash & Accounts")

    # Default admin credentials (change if needed)
    ADMIN_CREDENTIALS = {"username": "admin", "password": "admin123"}

    admin_user = st.text_input("Admin Username", key="admin_user")
    admin_pass = st.text_input("Admin Password", key="admin_pass", type="password")

    if not st.session_state["admin_logged_in"]:
        if st.button("Login as Admin", key="admin_login"):
            if admin_user == ADMIN_CREDENTIALS["username"] and admin_pass == ADMIN_CREDENTIALS["password"]:
                st.session_state["admin_logged_in"] = True
                st.success("✅ Admin login successful!")
            else:
                st.error("❌ Invalid admin credentials.")
    else:
        st.success("Logged in as Admin ✅")

        st.subheader("💸 Add Cash to ATM")
        denom = st.selectbox("Denomination to add", ["500","200","100","50"], key="admin_denom")
        cnt = st.number_input("Count", min_value=0, key="admin_count")
        if st.button("Add Cash", key="admin_add"):
            msg = admin_add_cash(admin_user, int(denom), int(cnt))
            st.success(msg)

        st.subheader("🏦 ATM Notes Status")
        cash_info = view_cash()
        st.table(cash_info["notes"])
        st.write(f"**Total in ATM:** ₹{cash_info['total']}")

        st.markdown("---")
        st.subheader("⚙️ Account Activation / Deactivation")
        acc = st.text_input("Account Number", key="admin_acc")
        act = st.selectbox("Action", ["activate","deactivate"], key="admin_action")
        if st.button("Apply Action", key="admin_apply"):
            if acc not in accounts:
                st.error("Account not found.")
            else:
                accounts[acc]["active"] = (act == "activate")
                save_accounts()
                st.success(f"✅ Account {acc} has been set to {act}.")

        if st.button("Logout Admin"):
            st.session_state["admin_logged_in"] = False
            st.success("👋 Admin logged out.")

# ----------------------------
# REPORTS PAGE
# ----------------------------
elif page == "Reports":
    st.header("📜 Transaction Reports")
    logs = view_reports(limit=1000)
    st.markdown("Most recent activity (latest first):")
    for log in reversed(logs[-200:]):
        st.write(log)

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("\n\n---\nMade with ⚔️ Swordigo theme — Streamlit ATM demo")
