import json
import os
from datetime import datetime
import jsonfile
import shiftdata

def clockIn():
    shiftdata.startShift()  

    with open("shiftdata.json", "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if data["ID"] == jsonfile.currentEmployeeID:
                return data.get("ClockInTime")

def clockOut():
    shiftdata.endShift()  

    # Read the correct employee's shift data
    shift = None
    with open("shiftdata.json", "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if data["ID"] == jsonfile.currentEmployeeID:
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

    total_minutes = (clock_out_time.hour * 60 + clock_out_time.minute) - \
                    (clock_in_time.hour * 60 + clock_in_time.minute)
    if total_minutes < 0:
        total_minutes += 24 * 60
    worked_hours = total_minutes // 60
    worked_minutes = total_minutes % 60

    # Read all records from hours.json
    hours_records = []
    employee_found = False

    if os.path.exists("hours.json"):
        with open("hours.json", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if record["ID"] == jsonfile.currentEmployeeID:
                        # Update the matching employee's record
                        record["TotalHoursWorked"] = record.get("TotalHoursWorked", 0) + int(worked_hours)
                        record["TotalMinutesWorked"] = record.get("TotalMinutesWorked", 0) + int(worked_minutes)
                        # Normalize minutes into hours
                        extra = record["TotalMinutesWorked"] // 60
                        record["TotalHoursWorked"] += extra
                        record["TotalMinutesWorked"] %= 60
                        employee_found = True
                    hours_records.append(json.dumps(record))
                except json.JSONDecodeError:
                    continue

    # If no record existed for this employee, create one
    if not employee_found:
        new_record = {
            "ID": jsonfile.currentEmployeeID,
            "TotalHoursWorked": int(worked_hours),
            "TotalMinutesWorked": int(worked_minutes)
        }
        hours_records.append(json.dumps(new_record))

    # Write all records back
    with open("hours.json", "w") as file:
        file.write("\n".join(hours_records) + "\n")

    return {
        "clock_in": clock_in_str,
        "clock_out": clock_out_str,
        "worked_hours": int(worked_hours),
        "worked_minutes": int(worked_minutes)
    }

""" For testing purposes only
def main():
    jsonfile.main()
    clockIn()
    clockOut()
    return 0

if __name__ == "__main__":
    main()
"""