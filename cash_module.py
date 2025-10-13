# cash_module.py
from storage import cash, save_cash, add_report
from datetime import datetime

def total_cash():
    return sum(int(denom) * count for denom, count in cash.items())

def show_cash_status():
    # return dict sorted by denomination descending (strings)
    return {k: cash[k] for k in sorted(cash.keys(), key=lambda x: int(x), reverse=True)}

def add_cash(admin_name, denom, count):
    if str(denom) not in cash:
        return "Invalid denomination."
    if count <= 0:
        return "Count must be > 0."
    cash[str(denom)] += int(count)
    save_cash()
    add_report(f"[{datetime.now()}] ADMIN {admin_name} added {count} x ₹{denom} notes. Total cash now: ₹{total_cash()}")
    return f"Added {count} x ₹{denom} notes successfully."

def can_dispense(amount):
    temp_cash = cash.copy()
    notes_to_give = {}
    remaining = int(amount)
    for denom in sorted(map(int, temp_cash.keys()), reverse=True):
        denom_s = str(denom)
        if remaining <= 0:
            break
        available = temp_cash[denom_s]
        take = min(remaining // denom, available)
        if take > 0:
            notes_to_give[denom] = take
            remaining -= denom * take
    if remaining == 0:
        return True, notes_to_give
    else:
        return False, {}

def dispense_notes(notes_to_give, user_name="UNKNOWN_USER"):
    for denom, count in notes_to_give.items():
        denom_s = str(denom)
        cash[denom_s] -= int(count)
    save_cash()
    add_report(f"[{datetime.now()}] USER {user_name} withdrew {sum(int(d)*int(c) for d,c in notes_to_give.items())} using {notes_to_give}")
