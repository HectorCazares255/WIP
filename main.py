import jsonfile
import shiftdata
from datetime import datetime

def clockIn():
    print("Would you like to clock in? (yes/no): ")
    clock_in_response = input()
    if clock_in_response.lower() == "yes":
        clock_in_time = datetime.now()
        #shift_start = (clock_in_time.hour * 60) + clock_in_time.minute # Converts shift start time to minutes
        clock_in = clock_in_time.strftime("%H:%M")
        print("Clocked in at:", clock_in)
        shiftdata.startShift()

def clockOut():
    print("Would you like to clock out? (yes/no): ")
    clock_out_response = input()
    if clock_out_response.lower() == "yes":
        clock_out_time = datetime.now()
        #shift_end = (clock_out_time.hour * 60) + clock_out_time.minute  # Converts shift end time to minutes
        #time_worked_hours = (shift_end - shift_start)/60    # Finds total hours worked
        #time_worked_minutes = (shift_end - shift_start)%60  # Finds remaining minutes worked
        clock_out = clock_out_time.strftime("%H:%M")
        print("Clocked out at:", clock_out)
        #print("Time worked:", int(time_worked_hours), "hour(s) and", time_worked_minutes, "minute(s)")
        shiftdata.endShift()

def main():
    ##jsonfile.main()
    shiftdata.checkShift()
    return 0


if __name__ == "__main__":
    main()