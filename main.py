import json
from datetime import datetime
import shiftdata

def clockIn():
    shiftdata.startShift()  
    with open("shiftdata.json", "r") as file:
        data = json.load(file)
    return data.get("ClockInTime")

def clockOut():
    shiftdata.endShift()  

    with open("shiftdata.json", "r") as file:
        data = json.load(file)

    clock_in_str = data.get("ClockInTime")
    clock_out_str = data.get("ClockOutTime")

    if not clock_in_str or not clock_out_str:
        raise ValueError("ClockInTime or ClockOutTime missing in shiftdata.json")

    clock_in_time = datetime.strptime(clock_in_str, "%H:%M")
    clock_out_time = datetime.strptime(clock_out_str, "%H:%M")

    start_min = clock_in_time.hour * 60 + clock_in_time.minute
    end_min = clock_out_time.hour * 60 + clock_out_time.minute

    total_minutes = end_min - start_min
    if total_minutes < 0:
        total_minutes += 24 * 60  
    worked_hours = total_minutes // 60
    worked_minutes = total_minutes % 60

    try:
        with open("hours.json", "r") as file:
            totals = json.load(file)
    except FileNotFoundError:
        totals = {"TotalHoursWorked": 0, "TotalMinutesWorked": 0}

    totals["TotalHoursWorked"] = totals.get("TotalHoursWorked", 0) + int(worked_hours)
    totals["TotalMinutesWorked"] = totals.get("TotalMinutesWorked", 0) + int(worked_minutes)

    # normalize minutes into hours
    extra = totals["TotalMinutesWorked"] // 60
    totals["TotalHoursWorked"] += extra
    totals["TotalMinutesWorked"] %= 60

    with open("hours.json", "w") as file:
        json.dump(totals, file, indent=2)

    return {
        "clock_in": clock_in_str,
        "clock_out": clock_out_str,
        "worked_hours": int(worked_hours),
        "worked_minutes": int(worked_minutes),
        "totals": totals
    }