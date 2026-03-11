import json
import os
import random

currentEmployeeID = 521207

# function is only for admins
def admin():
    name = input("Welcome Admin! Please enter your name: ")
    email = input("Please enter your email: ")
    password = input("Please enter your password: ")

    add_employee = input("Would you like to add an employee? (yes/no): ")
    if add_employee.lower() == "yes":
        addEmployee()
    elif add_employee.lower() == "no":
        print("No new employees added.")
    else:
        print("Invalid option!")

def addEmployee():
    occupation = "Employee"
    name = input("Please enter the employee's name: ")
    email = input("Please enter the employee's email: ")
    password = input("Please enter the employee's password?: ")
    id = random.randint(100000, 999999)

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
                return

        print("Invalid credentials. Please try again.")
    else:
        print("No employee records found.")

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