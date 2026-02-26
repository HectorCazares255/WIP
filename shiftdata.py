import json
import jsonfile
import os
from datetime import datetime

SHIFT_FILE = "shiftdata.json"

def _read_shift():
    if not os.path.exists(SHIFT_FILE):
        return {"ID": jsonfile.currentEmployeeID, "ClockedIn": "No"}
    try:
        with open(SHIFT_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                if data["ID"] == jsonfile.currentEmployeeID:
                    return data  # Exit once a match is found
    except json.JSONDecodeError:
        pass
    return {"ID": jsonfile.currentEmployeeID, "ClockedIn": "No"}  # No match found


def _write_shift(new_data):
    lines = []

    # Read all existing records
    if os.path.exists(SHIFT_FILE):
        with open(SHIFT_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    # Replace the matching record, keep everything else
                    if data["ID"] == jsonfile.currentEmployeeID:
                        lines.append(json.dumps(new_data))
                    else:
                        lines.append(json.dumps(data))
                except json.JSONDecodeError:
                    continue
    
    # If no existing record was found for this employee, append a new one
    if not any(json.loads(l).get("ID") == jsonfile.currentEmployeeID for l in lines):
        lines.append(json.dumps(new_data))

    with open(SHIFT_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")


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