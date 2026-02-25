import json
import os
from flask import Flask, render_template, redirect, url_for
import shiftdata
from main import clockIn, clockOut

app = Flask(__name__)

def read_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default

@app.route("/")
def index():
    shift = read_json("shiftdata.json", {})
    totals = read_json("hours.json", {"TotalHoursWorked": 0, "TotalMinutesWorked": 0})

    return render_template(
        "index.html",
        clocked_in=shift.get("ClockedIn", "No"),
        clock_in=shift.get("ClockInTime"),
        clock_out=shift.get("ClockOutTime"),
        total_hours=totals.get("TotalHoursWorked", 0),
        total_minutes=totals.get("TotalMinutesWorked", 0),
    )

@app.route("/clock-in", methods=["POST"])
def clock_in():
    if shiftdata.checkShift() == "Yes":
        return "Already clocked in.", 400
    clockIn()
    return redirect(url_for("index"))

@app.route("/clock-out", methods=["POST"])
def clock_out():
    if shiftdata.checkShift() == "No":
        return "You are not clocked in.", 400
    clockOut()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)