# admin_module.py
from storage import accounts, save_accounts, reports, load_reports
from cash_module import show_cash_status, total_cash, add_cash

def admin_module(acc, action):
    if acc not in accounts:
        return "Account not found."
    if action.lower() == "activate": accounts[acc]["active"] = True
    elif action.lower() == "deactivate": accounts[acc]["active"] = False
    else: return "Invalid action."
    save_accounts()
    return f"Account {acc} {action}d."

def admin_add_cash(name, denom, count):
    return add_cash(name, denom, count)

def view_cash():
    data = show_cash_status()
    total = total_cash()
    return {"notes": data, "total": total}

def view_reports(limit=200):
    load_reports()
    return reports[-limit:]
