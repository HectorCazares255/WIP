import json
import os
from datetime import datetime

SHIFT_FILE = "shiftdata.json"


def read_shift_file():
    if not os.path.exists(SHIFT_FILE):
        return []
    try:
        with open(SHIFT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def write_shift_file(data):
    with open(SHIFT_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _read_shift(employee_id):
    records = read_shift_file()

    for data in records:
        if data.get("ID") == employee_id:
            return data

    return {"ID": employee_id, "ClockedIn": "No"}


def _write_shift(employee_id, new_data):
    records = read_shift_file()
    updated = False

    for i, data in enumerate(records):
        if data.get("ID") == employee_id:
            records[i] = new_data
            updated = True
            break

    if not updated:
        records.append(new_data)

    write_shift_file(records)


def startShift(employee_id):
    data = _read_shift(employee_id)
    data["ClockedIn"] = "Yes"
    data["ClockInTime"] = datetime.now().strftime("%H:%M")
    data["ClockOutTime"] = ""
    _write_shift(employee_id, data)


def endShift(employee_id):
    data = _read_shift(employee_id)
    data["ClockedIn"] = "No"
    data["ClockOutTime"] = datetime.now().strftime("%H:%M")
    _write_shift(employee_id, data)


def checkShift(employee_id):
    data = _read_shift(employee_id)
    return data.get("ClockedIn", "No")