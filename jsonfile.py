import json
import os
import random

#function is only for admins
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

    #saves answers in a dictionary
    employee_data = { "Occupation": occupation, "Name": name, "Email": email, "Password": password, "ID": id }

    #checking if the JSON file exists, if it does, we dump dictionary info inside
    if os.path.exists("employeeinfo.json"):
        with open("employeeinfo.json", "a") as file:
            json.dump(employee_data, file)
            file.write("\n")  # Add newline for readability

    #if JSON file does not exist, we create the JSON file
    else:
        print("Error occurred. Trying again...")
        with open("employeeinfo.json", "w") as file:
            json.dump(employee_data, file)

#this function is only for employees
def employee():
    name = input("Welcome! Please enter your name: ")
    email = input("Please enter your email: ")
    password = input("Please enter your password?: ")

    if os.path.exists("employeeinfo.json"):
        with open("employeeinfo.json", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)  # json.loads() for a single line string
                if name == data["Name"] and email == data["Email"] and password == data["Password"]:
                    print("Welcome back", name + "!")
                    global currentEmployeeID
                    currentEmployeeID = data["ID"]
                    return  # Exit once a match is found
            print("Invalid credentials. Please try again.")
    else:
        print("No employee records found.")

def main():
    #asks if user is admin or employee
    jobchoice = input("Are you an admin or employee?: ")

    #if they are an admin, it goes to the admin function
    if jobchoice.lower() == "admin":
        admin()
    #if employee, then it goes to employee function
    elif jobchoice.lower() == "employee":
        employee()
    #invalid choice if they didn't write any of the choices above
    else:
        print("Invalid choice!")
    
    return 0

if __name__ == "__main__":
    main()