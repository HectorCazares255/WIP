import json
import os
from flask import Flask, render_template, redirect, url_for, request, session
import shiftdata
from main import clockIn, clockOut

app = Flask(__name__)
app.secret_key = "your_secret_key_here"


def read_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default


def find_employee_record(records, employee_id):
    if not isinstance(records, list):
        return {}

    for record in records:
        if record.get("ID") == employee_id:
            return record

    return {}


def find_employee_by_credentials(email, password):
    employees = read_json("employeeinfo.json", [])

    for employee in employees:
        if employee.get("Email") == email and employee.get("Password") == password:
            return employee

    return None

def load_shift_data():
    if not os.path.exists("shiftdata.json"):
        return []

    with open("shiftdata.json", "r") as file:
        return json.load(file)

def load_employees():
    if not os.path.exists("employeeinfo.json"):
        return []

    with open("employeeinfo.json", "r") as file:
        return json.load(file)
    

def get_clocked_in_employees():
    employees = load_employees()
    shift_data = load_shift_data()

    clocked_in_list = []

    for shift in shift_data:
        if shift.get("ClockedIn") == "Yes":
            employee_id = shift.get("ID")

            for employee in employees:
                if employee["ID"] == employee_id:
                    clocked_in_list.append({
                        "ID": employee["ID"],
                        "Name": employee["Name"],
                        "Email": employee["Email"],
                        "ClockInTime": shift.get("ClockInTime", "—")
                    })
                    break

    return clocked_in_list
    
    
def save_employees(employees):
    with open("employeeinfo.json", "w") as file:
        json.dump(employees, file, indent=2)  




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with open("employeeinfo.json", "r") as file:
            employees = json.load(file)

        for employee in employees:
            if employee["Email"] == email and employee["Password"] == password:
                session["employee_id"] = employee["ID"]
                session["employee_name"] = employee["Name"]
                session["employee_occupation"] = employee["Occupation"]
                return redirect(url_for("index"))

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    if "employee_id" not in session:
        return redirect(url_for("login"))

    current_id = session["employee_id"]
    current_name = session.get("employee_name", "Employee")

    shifts = read_json("shiftdata.json", [])
    totals_list = read_json("hours.json", [])

    shift = find_employee_record(shifts, current_id)
    totals = find_employee_record(totals_list, current_id)

    return render_template(
        "index.html",
        employee_name=current_name,
        clocked_in=shift.get("ClockedIn", "No"),
        clock_in=shift.get("ClockInTime", ""),
        clock_out=shift.get("ClockOutTime", ""),
        total_hours=totals.get("TotalHoursWorked", 0),
        total_minutes=totals.get("TotalMinutesWorked", 0),
    )


@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    if "employee_id" not in session:
        return redirect(url_for("login"))

    if session.get("employee_occupation") != "Admin":
        return "Access denied. Admins only."

    message = None
    error = None

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        occupation = request.form["occupation"]
        employee_id = request.form["id"]

        employees = load_employees()

        for employee in employees:
            if employee["Email"] == email:
                error = "An account with that email already exists."
                break

        if not error:
            for employee in employees:
                if str(employee["ID"]) == str(employee_id):
                    error = "An account with that ID already exists."
                    break

        if not error:
            new_employee = {
                "ID": int(employee_id),
                "Name": name,
                "Email": email,
                "Password": password,
                "Occupation": occupation
            }

            employees.append(new_employee)
            save_employees(employees)
            message = "Employee account created successfully."

    clocked_in_employees = get_clocked_in_employees()

    return render_template(
        "admin.html",
        admin_name=session.get("employee_name"),
        clocked_in_employees=clocked_in_employees,
        message=message,
        error=error
    )



@app.route("/clock-in", methods=["POST"])
def clock_in():
    if "employee_id" not in session:
        return redirect(url_for("login"))

    if shiftdata.checkShift(session["employee_id"]) == "Yes":
        return "Already clocked in.", 400

    clockIn(session["employee_id"])
    return redirect(url_for("index"))


@app.route("/clock-out", methods=["POST"])
def clock_out():
    if "employee_id" not in session:
        return redirect(url_for("login"))

    if shiftdata.checkShift(session["employee_id"]) == "No":
        return "You are not clocked in.", 400

    clockOut(session["employee_id"])
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)