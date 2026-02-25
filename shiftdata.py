import json
import main
import os
from datetime import datetime

SHIFT_FILE = "shiftdata.json"

def _read_shift():
    if not os.path.exists(SHIFT_FILE):
        return {"ClockedIn": "No"}
    try:
        with open(SHIFT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"ClockedIn": "No"}

def _write_shift(data):
    with open(SHIFT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def startShift():
    data = _read_shift()
    data["ClockedIn"] = "Yes"
    data["ClockInTime"] = datetime.now().strftime("%H:%M")
    _write_shift(data)

def endShift():
    data = _read_shift()
    data["ClockedIn"] = "No"
    data["ClockOutTime"] = datetime.now().strftime("%H:%M")
    _write_shift(data)

def checkShift():
    data = _read_shift()
    return data.get("ClockedIn", "No")   