# storage.py
# Handles account storage, cash storage and reports storage

from datetime import datetime

accounts = {}
cash = {"500": 20, "200": 30, "100": 50, "50": 100}  # default stock
reports = []  # list of report strings

def load_accounts():
    global accounts
    try:
        with open("accounts.txt", "r") as f:
            accounts.clear()
            for line in f:
                line = line.strip()
                if not line: continue
                acc_no, name, pin, balance, active = line.split(",")
                accounts[acc_no] = {
                    "name": name,
                    "pin": pin,
                    "balance": float(balance),
                    "active": active == "True"
                }
    except FileNotFoundError:
        accounts = {}

def save_accounts():
    with open("accounts.txt", "w") as f:
        for acc_no, info in accounts.items():
            f.write(f"{acc_no},{info['name']},{info['pin']},{info['balance']},{info['active']}\n")

def load_cash():
    global cash
    try:
        with open("cash.txt", "r") as f:
            cash.clear()
            for line in f:
                line = line.strip()
                if not line: continue
                denom, count = line.split(",")
                cash[denom] = int(count)
    except FileNotFoundError:
        save_cash()  # create default file

def save_cash():
    with open("cash.txt", "w") as f:
        for denom, count in cash.items():
            f.write(f"{denom},{count}\n")

def load_reports():
    global reports
    try:
        with open("reports.txt", "r") as f:
            reports[:] = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        reports.clear()

def add_report(entry):
    # entry should be a string; we'll prefix with timestamp if not present
    ts = entry
    if not entry.startswith("["):
        ts = f"[{datetime.now()}] {entry}"
    reports.append(ts)
    with open("reports.txt", "a") as f:
        f.write(ts + "\n")
