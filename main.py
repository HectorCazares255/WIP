from datetime import datetime

def main():
    choice = input("Would you like to clock in? (yes/no): ")
    if choice.lower() == "yes":
        clock_in_time = datetime.now()
        shift_start = (clock_in_time.hour * 60) + clock_in_time.minute # Converts shift start time to minutes
        if clock_in_time.minute <= 9:  # Adds leading zero for single digit minutes
            clock_in = str(clock_in_time.hour) + ":" + "0" + str(clock_in_time.minute)
            print("Clocked in at:", clock_in)
        else:
            clock_in = str(clock_in_time.hour) + ":" + str(clock_in_time.minute)
            print("Clocked in at:", clock_in)
    
    choice = input("Would you like to clock out? (yes/no): ")
    if choice.lower() == "yes":
        clock_out_time = datetime.now()
        shift_end = (clock_out_time.hour * 60) + clock_out_time.minute  # Converts shift end time to minutes
        time_worked_hours = (shift_end - shift_start)/60    # Finds total hours worked
        time_worked_minutes = (shift_end - shift_start)%60  # Finds remaining minutes worked
        if clock_out_time.minute <= 9:  # Adds leading zero for single digit minutes
            clock_out = str(clock_out_time.hour) + ":" + "0" + str(clock_out_time.minute)
            print("Clocked out at:", clock_out)
        else:
            clock_out = str(clock_out_time.hour) + ":" + str(clock_out_time.minute)
            print("Clocked out at:", clock_out)
        print("Time worked:", int(time_worked_hours), "hour(s) and", time_worked_minutes, "minute(s)")
    return 0


if __name__ == "__main__":
    main()