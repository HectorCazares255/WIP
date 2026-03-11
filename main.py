import json
import os
from datetime import datetime
import shiftdata

HOURS_FILE = "hours.json"
SHIFT_FILE = "shiftdata.json"


def read_json_file(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return default


def write_json_file(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


def clockIn(employee_id):
    shiftdata.startShift(employee_id)

    shifts = read_json_file(SHIFT_FILE, [])
    for data in shifts:
        if data.get("ID") == employee_id:
            return data.get("ClockInTime")

    return None


def clockOut(employee_id):
    shiftdata.endShift(employee_id)

    shifts = read_json_file(SHIFT_FILE, [])
    shift = None

    for data in shifts:
        if data.get("ID") == employee_id:
            shift = data
            break

    if not shift:
        raise ValueError("No shift record found for current employee.")

    clock_in_str = shift.get("ClockInTime")
    clock_out_str = shift.get("ClockOutTime")

    if not clock_in_str or not clock_out_str:
        raise ValueError("ClockInTime or ClockOutTime missing in shiftdata.json")

    clock_in_time = datetime.strptime(clock_in_str, "%H:%M")
    clock_out_time = datetime.strptime(clock_out_str, "%H:%M")

    total_minutes = (
        (clock_out_time.hour * 60 + clock_out_time.minute)
        - (clock_in_time.hour * 60 + clock_in_time.minute)
    )

    if total_minutes < 0:
        total_minutes += 24 * 60

    worked_hours = total_minutes // 60
    worked_minutes = total_minutes % 60

    hours_records = read_json_file(HOURS_FILE, [])
    employee_found = False

    for record in hours_records:
        if record.get("ID") == employee_id:
            record["TotalHoursWorked"] = record.get("TotalHoursWorked", 0) + int(worked_hours)
            record["TotalMinutesWorked"] = record.get("TotalMinutesWorked", 0) + int(worked_minutes)

            extra = record["TotalMinutesWorked"] // 60
            record["TotalHoursWorked"] += extra
            record["TotalMinutesWorked"] %= 60

            employee_found = True
            break

    if not employee_found:
        new_record = {
            "ID": employee_id,
            "TotalHoursWorked": int(worked_hours),
            "TotalMinutesWorked": int(worked_minutes)
        }
        hours_records.append(new_record)

    write_json_file(HOURS_FILE, hours_records)

    return {
        "clock_in": clock_in_str,
        "clock_out": clock_out_str,
        "worked_hours": int(worked_hours),
        "worked_minutes": int(worked_minutes)
    }