import json
import jsonfile
import shiftdata
from datetime import datetime

# Clock in function that checks if the employee wants to clock in and calls the start shift function
def clockIn():
    print("Would you like to clock in? (yes/no): ")
    clock_in_response = input()
    if clock_in_response.lower() == "yes":
        shiftdata.startShift()
        clock_in_time = datetime.now()
        clock_in = clock_in_time.strftime("%H:%M")
        print("Clocked in at:", clock_in)

# Clock out function that checks if the employee wants to clock out and calls the end shift function, also calculates total time worked
def clockOut():
    print("Would you like to clock out? (yes/no): ")
    clock_out_response = input()
    if clock_out_response.lower() == "yes":
        shiftdata.endShift()
        clock_out_time = datetime.now()
        with open("shiftdata.json", "r") as file: # Reads the JSON file to get the clock in and clock out time
            data = json.load(file)
            clock_in_time = datetime.strptime(data["ClockInTime"], "%H:%M")
            clock_out_time = datetime.strptime(data["ClockOutTime"], "%H:%M")
        shift_start = (clock_in_time.hour * 60) + clock_in_time.minute # Converts shift start time to minutes
        shift_end = (clock_out_time.hour * 60) + clock_out_time.minute  # Converts shift end time to minutes
        time_worked_hours = (shift_end - shift_start)/60    # Finds total hours worked
        time_worked_minutes = (shift_end - shift_start)%60  # Finds remaining minutes worked
        clock_out = clock_out_time.strftime("%H:%M")

        # Updates the total hours worked in the JSON file
        with open("hours.json", "r") as file: # Reads the JSON file to get the total hours worked
            data = json.load(file)
            total_hours_worked = data.get("TotalHoursWorked", 0)
            total_minutes_worked = data.get("TotalMinutesWorked", 0)
        total_hours_worked += int(time_worked_hours) # Adds the hours worked to the total hours worked
        total_minutes_worked += time_worked_minutes # Adds the minutes worked to the total minutes worked
        with open("hours.json", "w") as file: # Writes the total hours worked to the JSON file
            json.dump({"TotalHoursWorked": total_hours_worked, "TotalMinutesWorked": total_minutes_worked}, file)

        print("Clocked out at:", clock_out)
        print("Time worked:", int(time_worked_hours), "hour(s) and", time_worked_minutes, "minute(s)")

def main():
    ##jsonfile.main()
    shiftdata.checkShift()
    return 0


if __name__ == "__main__":
    main()