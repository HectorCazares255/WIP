import json
import os
from datetime import datetime
import shiftdata

HOURS_FILE = "hours.json"
SHIFT_FILE = "shiftdata.json"
EMPLOYEE_FILE = "employeeinfo.json"


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

def checkShiftTime(employee_id):
    # This function will check the current time and compare it to the schedule of the employee
    # If it isn't time for the employee to work, it will not allow them to clock in
    # If it is past time for the employee to clock out, it will give them a warning
    id = employee_id
    schedule_file = "schedule.json"
    if os.path.exists(schedule_file):
        try:
            with open(schedule_file, "r") as file:
                schedules = json.load(file)
        except json.JSONDecodeError:
            print("Schedule file is corrupted.")
            return False
        for schedule in schedules:
            if schedule.get("ID") == int(id):
                current_day = datetime.now().strftime("%A")
                current_time = datetime.now().strftime("%H:%M")
                scheduled_time = schedule.get(current_day)
                if scheduled_time == "Off":
                    print("You are not scheduled to work today.")
                    return False
                # Converts the current time and scheduled time to minutes for easier comparison
                elif int(current_time.split(":")[0]) * 60 + int(current_time.split(":")[1]) < int(scheduled_time.split("-")[0].split(":")[0]) * 60 + int(scheduled_time.split("-")[0].split(":")[1]):
                    print("It is not time for you to work yet. You are scheduled for ", scheduled_time)
                    return False
                elif int(current_time.split(":")[0]) * 60 + int(current_time.split(":")[1]) > int(scheduled_time.split("-")[1].split(":")[0]) * 60 + int(scheduled_time.split("-")[1].split(":")[1]):
                    print("You are past your scheduled time to work. Please clock out immediately.")
                    return True
                else:
                    return True
        else:
            print("Employee ID not found in schedule records.")
            return False

def clockIn(employee_id):
    if not checkShiftTime(employee_id):
        return None

    shiftdata.startShift(employee_id)

    shifts = read_json_file(SHIFT_FILE, [])
    for data in shifts:
        if data.get("ID") == employee_id:
            return data.get("ClockInTime")

    return None


def clockOut(employee_id):
    if not checkShiftTime(employee_id):
        return None

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

    print(f"Total worked time: {worked_hours} hours and {worked_minutes} minutes.")
    payment_records = read_json_file(EMPLOYEE_FILE, [])
    for employee in payment_records:
        if employee.get("ID") == employee_id:
            hourly_rate = employee.get("HourlyRate")
            print(f"Money earned: ${worked_hours * hourly_rate + (worked_minutes / 60) * hourly_rate:.2f}")
            break

    return {
        "clock_in": clock_in_str,
        "clock_out": clock_out_str,
        "worked_hours": int(worked_hours),
        "worked_minutes": int(worked_minutes)
    }