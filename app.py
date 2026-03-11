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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        employee = find_employee_by_credentials(email, password)

        if employee:
            session["employee_id"] = employee.get("ID")
            session["employee_name"] = employee.get("Name")
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid email or password.")

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