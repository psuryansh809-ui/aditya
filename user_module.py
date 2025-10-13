# user_module.py
# Console helpers - optional for CLI use
from storage import accounts, save_accounts

def register_user_console():
    print("--- Register New User (console) ---")
    acc_no = input("Account Number: ").strip()
    if acc_no in accounts:
        print("Account already exists.")
        return
    name = input("Name: ").strip()
    pin = input("4-digit PIN: ").strip()
    if len(pin) != 4 or not pin.isdigit():
        print("Invalid PIN. Must be 4 digits.")
        return
    try:
        bal = float(input("Initial deposit: ").strip())
    except:
        print("Invalid amount.")
        return
    accounts[acc_no] = {"name": name, "pin": pin, "balance": bal, "active": True}
    save_accounts()
    print(f"Registered {acc_no}.")
