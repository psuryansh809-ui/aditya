# main.py - Streamlit Swordigo-themed ATM Dashboard
import streamlit as st
from storage import load_accounts, load_cash, load_reports, accounts
from storage import save_accounts
from admin_module import admin_add_cash, view_cash, view_reports
from account_module import withdraw, deposit, current_balance, transfer_funds
from datetime import datetime

# Load data files if present
load_accounts()
load_cash()
load_reports()

st.set_page_config(page_title="Swordigo ATM", page_icon="⚔️", layout="wide")

# Swordigo-like CSS (simple)
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

st.title("⚔️ Swordigo ATM Dashboard")
st.write("Welcome — use the sidebar to navigate. After a user performs one transaction they must login again for the next task.")

side = st.sidebar

page = side.radio("Menu", ["Home", "Login", "Register", "Admin", "Reports"]) 

if page == "Home":
    st.header("ATM Overview")
    cash_info = view_cash()
    cols = st.columns([2,1])
    with cols[0]:
        st.subheader("ATM Notes Status")
        st.table(cash_info["notes"])
    with cols[1]:
        st.subheader("Total Cash")
        st.metric("Total in ATM", f"₹{cash_info['total']}")

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
            st.success(f"Account {acc_no} created for {name}.")

elif page == "Login": 
    st.header("User Login (one action per login)")
    acc_no = st.text_input("Account Number", key="login_acc")
    pin = st.text_input("PIN", key="login_pin", type="password")
    if st.button("Login"):
        if acc_no in accounts and accounts[acc_no]["pin"] == pin:
            if not accounts[acc_no]["active"]:
                st.error("Account is deactivated.")
            else:
                st.success(f"Welcome {accounts[acc_no]['name']} — pick one action.")
                # show four big buttons for actions
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    if st.button("🏧 Withdraw", key="btn_withdraw"):
                        amt = st.number_input("Amount to withdraw", min_value=0, step=10, key="withdraw_amt")
                        # desired notes selection (optional)
                        if st.button("Confirm Withdraw", key="confirm_withdraw"):
                            res = withdraw(acc_no, int(amt))
                            st.info(res)
                            st.warning("You have been logged out. Login again for another task.")
                with c2:
                    if st.button("💰 Deposit", key="btn_deposit"):
                        damt = st.number_input("Amount to deposit", min_value=0.0, step=10.0, key="deposit_amt")
                        if st.button("Confirm Deposit", key="confirm_deposit"):
                            res = deposit(acc_no, float(damt))
                            st.info(res)
                            st.warning("You have been logged out. Login again for another task.")
                with c3:
                    if st.button("📄 Check Balance", key="btn_balance"):
                        res = current_balance(acc_no)
                        st.info(res)
                        st.warning("You have been logged out. Login again for another task.")
                with c4:
                    if st.button("🔁 Transfer", key="btn_transfer"):
                        recv = st.text_input("Receiver Account No.", key="transfer_recv")
                        tamt = st.number_input("Amount", min_value=0.0, key="transfer_amt")
                        if st.button("Confirm Transfer", key="confirm_transfer"):
                            res = transfer_funds(acc_no, recv, float(tamt))
                            st.info(res)
                            st.warning("You have been logged out. Login again for another task.")
        else:
            st.error("Invalid credentials or account not found.")

elif page == "Admin": 
    st.header("Admin Panel — manage cash & accounts")
    name = st.text_input("Admin Name", key="admin_name")
    denom = st.selectbox("Denomination to add", ["500","200","100","50"], key="admin_denom")
    cnt = st.number_input("Count", min_value=0, key="admin_count")
    if st.button("Add Cash", key="admin_add"):
        if not name:
            st.error("Enter admin name.")
        else:
            msg = admin_add_cash(name, int(denom), int(cnt))
            st.success(msg)
    st.subheader("ATM Notes Status")
    cash_info = view_cash()
    st.table(cash_info["notes"])
    st.write(f"**Total in ATM:** ₹{cash_info['total']}")
    st.markdown("---")
    st.subheader("Account Activation/Deactivation (Admin)")
    acc = st.text_input("Account Number to modify", key="admin_acc")
    act = st.selectbox("Action", ["activate","deactivate"], key="admin_action")
    if st.button("Apply Action", key="admin_apply"):
        if acc not in accounts:
            st.error("Account not found.")
        else:
            accounts[acc]["active"] = (act == "activate")
            save_accounts()
            st.success(f"Account {acc} set to {act}.")

elif page == "Reports": 
    st.header("Transaction Reports")
    logs = view_reports(limit=1000)
    st.markdown("Most recent activity (latest first):")
    for log in reversed(logs[-200:]):
        st.write(log)

st.markdown("\n\n---\nMade with ⚔️ Swordigo theme — Streamlit ATM demo") 
