import json
import os
import random

currentEmployeeID = 521207

# function is only for admins
def admin():
    name = input("Welcome Admin! Please enter your name: ")
    email = input("Please enter your email: ")
    password = input("Please enter your password: ")

    # Check if the admin credentials are correct
    if os.path.exists("employeeinfo.json"):
        with open("employeeinfo.json", "r") as file:
            employees = json.load(file)
        for employee in employees:
            if employee.get("Occupation") == "Admin" and employee.get("Name") == name and employee.get("Email") == email and employee.get("Password") == password:
                print("Admin credentials verified.")
                break
        else:
            print("Invalid admin credentials.")
            return
    else:
        print("No employee records found.")
        return
    
    add_employee = input("Would you like to add an employee? (yes/no): ")
    if add_employee.lower() == "yes":
        addEmployee()
    elif add_employee.lower() == "no":
        print("No new employees added.")
    else:
        print("Invalid option!")

    change_schedule = input("Would you like to change an employee's schedule? (yes/no): ")
    if change_schedule.lower() == "yes":
        changeSchedule()
    elif change_schedule.lower() == "no":
        print("No schedule changes made.")
    else:
        print("Invalid option!")
    
    pay_employees = input("Would you like to pay employees? (yes/no): ")
    if pay_employees.lower() == "yes":
        payEmployees()
    elif pay_employees.lower() == "no":
        print("Employees have not been paid.")

#function to add employees, which contains their occupation, name, email, password, and ID
def addEmployee():
    occupation = "Employee"
    name = input("Please enter the employee's name: ")
    email = input("Please enter the employee's email: ")
    password = input("Please enter the employee's password?: ")
    id = random.sample(range(100000, 999999), 1)

    #dictionary stores the info
    employee_data = {
        "Occupation": occupation,
        "Name": name,
        "Email": email,
        "Password": password,
        "ID": id
    }

    employees = []

    if os.path.exists("employeeinfo.json"):
        try:
            with open("employeeinfo.json", "r") as file:
                employees = json.load(file)
        except json.JSONDecodeError:
            employees = []

    employees.append(employee_data)

    with open("employeeinfo.json", "w") as file:
        json.dump(employees, file, indent=2)

# This function will allow the admin to change the schedule of an employee
def changeSchedule():
    id = input("Please enter the employee's ID: ")

    #prints out the current schedule for the employee, so the admin can see what they are changing
    print("Current schedule for employee ID", id + ":")
    schedule_file = "schedule.json"
    if os.path.exists(schedule_file):
        try:
            with open(schedule_file, "r") as file:
                schedules = json.load(file)
        except json.JSONDecodeError:
            print("Schedule file is corrupted.")
            return
        for schedule in schedules:
            if schedule.get("ID") == int(id):
                print("Monday:", schedule.get("Monday"))
                print("Tuesday:", schedule.get("Tuesday"))
                print("Wednesday:", schedule.get("Wednesday"))
                print("Thursday:", schedule.get("Thursday"))
                print("Friday:", schedule.get("Friday"))
                print("Saturday:", schedule.get("Saturday"))
                print("Sunday:", schedule.get("Sunday"))
                break
        else:
            print("Employee ID not found in schedule records.")
            return
        
    day = input("Please enter the day of the week to change (e.g., Monday): ")
    new_schedule = input("Please enter the new schedule (e.g., 9:00-17:00 or Off): ")
    schedule_file = "schedule.json"
    if os.path.exists(schedule_file):
        try:
            with open(schedule_file, "r") as file:
                schedules = json.load(file)
        except json.JSONDecodeError:
            schedules = []
        for schedule in schedules:
            if schedule.get("ID") == int(id):
                schedule[day] = new_schedule
                break
        else:
            print("Employee ID not found in schedule records.")
            return
        with open(schedule_file, "w") as file:
            json.dump(schedules, file, indent=2)
    else:
        print("Schedule file not found. No changes made.")

def payEmployees():
    #function to pay employees, which will be used by the admin
    if os.path.exists("hours.json"):
        with open("hours.json", "r") as file:
            hours_data = json.load(file)
        for record in hours_data:
            record["TotalHoursWorked"] = 0
            record["TotalMinutesWorked"] = 0
        with open("hours.json", "w") as file:            
            json.dump(hours_data, file, indent=2)
        print("Employees have been paid!")
    else:
        print("No hours data found.")

def getSchedule(id):
    #prints out the current schedule for the employee, so the employee can see when they are working
    print("Current schedule for employee ID", id , ":")
    schedule_file = "schedule.json"
    if os.path.exists(schedule_file):
        try:
            with open(schedule_file, "r") as file:
                schedules = json.load(file)
        except json.JSONDecodeError:
            print("Schedule file is corrupted.")
            return
        for schedule in schedules:
            if schedule.get("ID") == int(id):
                print("Monday:", schedule.get("Monday"))
                print("Tuesday:", schedule.get("Tuesday"))
                print("Wednesday:", schedule.get("Wednesday"))
                print("Thursday:", schedule.get("Thursday"))
                print("Friday:", schedule.get("Friday"))
                print("Saturday:", schedule.get("Saturday"))
                print("Sunday:", schedule.get("Sunday"))
                break
        else:
            print("Employee ID not found in schedule records.")
            return
        
#function that runs when the person picks employee
def employee():
    global currentEmployeeID

    name = input("Welcome! Please enter your name: ")
    email = input("Please enter your email: ")
    password = input("Please enter your password?: ")

    if os.path.exists("employeeinfo.json"):
        try:
            with open("employeeinfo.json", "r") as file:
                employees = json.load(file)
        except json.JSONDecodeError:
            employees = []
        
        for data in employees:
            if (
                name == data.get("Name") and
                email == data.get("Email") and
                password == data.get("Password")
            ):
                print("Welcome back", name + "!")
                currentEmployeeID = data["ID"]

                get_schedule = input("Would you like to view your schedule? (yes/no): ")
                if get_schedule.lower() == "yes":
                    getSchedule(currentEmployeeID)
                elif get_schedule.lower() == "no":
                    print("No schedule displayed.")
                else:
                    print("Invalid option!")

                return

        print("Invalid credentials. Please try again.")
    else:
        print("No employee records found.")

#main function, where tou decide if you're an admin or employee accordingly
def main():
    jobchoice = input("Are you an admin or employee?: ")

    if jobchoice.lower() == "admin":
        admin()
    elif jobchoice.lower() == "employee":
        employee()
    else:
        print("Invalid choice!")

    return 0

if __name__ == "__main__":
    main()