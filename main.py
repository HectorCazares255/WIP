from datetime import datetime

def main():
    choice = input("Would you like to clock in? (yes/no): ")
    if choice.lower() == "yes":
        current_time = datetime.now()
        print("Clocked in at:", current_time.hour, ":", current_time.minute)
        return current_time
    return 0


if __name__ == "__main__":
    main()