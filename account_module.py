# account_module.py
from storage import accounts, save_accounts, add_report
from cash_module import can_dispense, dispense_notes
from datetime import datetime

def is_active(account_no):
    return accounts.get(account_no, {}).get("active", False)

def withdraw(account_no, amount):
    if account_no not in accounts:
        return "Account not found."
    if not is_active(account_no):
        return "Account deactivated."
    try:
        amount = int(amount)
    except Exception:
        return "Invalid amount."
    if amount <= 0:
        return "Invalid amount."
    if accounts[account_no]["balance"] < amount:
        return "Insufficient account balance."

    ok, notes = can_dispense(amount)
    if not ok:
        return "ATM does not have notes to dispense this exact amount. Try different amount."

    accounts[account_no]["balance"] -= amount
    save_accounts()
    dispense_notes(notes, accounts[account_no]["name"])
    add_report(f"[{datetime.now()}] USER {accounts[account_no]['name']} withdrew ₹{amount}")
    note_info = ", ".join([f"{cnt}x₹{denom}" for denom, cnt in notes.items()])
    return f"₹{amount} withdrawn. Notes: {note_info}. New balance: ₹{accounts[account_no]['balance']:.2f}"

def deposit(account_no, amount):
    if account_no not in accounts:
        return "Account not found."
    if not is_active(account_no):
        return "Account deactivated."
    try:
        amount = float(amount)
    except Exception:
        return "Invalid amount."
    if amount <= 0:
        return "Invalid amount."
    accounts[account_no]["balance"] += amount
    save_accounts()
    add_report(f"[{datetime.now()}] USER {accounts[account_no]['name']} deposited ₹{amount}")
    return f"₹{amount} deposited. New balance: ₹{accounts[account_no]['balance']:.2f}"

def current_balance(account_no):
    if account_no not in accounts:
        return "Account not found."
    if not is_active(account_no):
        return "Account deactivated."
    return f"Current balance: ₹{accounts[account_no]['balance']:.2f}"

def transfer_funds(sender_no, receiver_no, amount):
    if sender_no not in accounts or receiver_no not in accounts:
        return "Sender or receiver account not found."
    if not is_active(sender_no):
        return "Sender account deactivated."
    if not is_active(receiver_no):
        return "Receiver account deactivated."
    try:
        amount = float(amount)
    except Exception:
        return "Invalid amount."
    if amount <= 0:
        return "Invalid amount."
    if accounts[sender_no]["balance"] < amount:
        return "Insufficient balance."
    accounts[sender_no]["balance"] -= amount
    accounts[receiver_no]["balance"] += amount
    save_accounts()
    add_report(f"[{datetime.now()}] USER {accounts[sender_no]['name']} transferred ₹{amount} to {accounts[receiver_no]['name']}")
    return f"₹{amount} transferred from {accounts[sender_no]['name']} to {accounts[receiver_no]['name']}"
