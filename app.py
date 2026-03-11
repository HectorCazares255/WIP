from datetime import datetime
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

shift_start_minutes = None
clock_in_time_str = None

@app.route("/")
def index():
    return render_template("index.html", clock_in_time=clock_in_time_str,)


@app.route("/clock_in", methods=["POST"])
def clock_in():
    global shift_start_minutes, clock_in_time_str

    now = datetime.now()
    shift_start_minutes = now.hour * 60 + now.minute
    clock_in_time_str = now.strftime("%H:%M:%S")

    return redirect(url_for("index"))


@app.route("/clock_out", methods=["POST"])
def clock_out():
    global shift_start_minutes, clock_in_time_str

    if shift_start_minutes is None:
        return "You must be clocked in before clocking out.", 400

    now = datetime.now()
    shift_end_minutes = now.hour * 60 + now.minute

    total_minutes = shift_end_minutes - shift_start_minutes
    hours = total_minutes // 60
    minutes = total_minutes % 60

    clock_out_time_str = now.strftime("%H:%M:%S")
    result = f"Clocked out at: {clock_out_time_str}"
             
    
    #Reset
    shift_start_minutes = None
    clock_in_time_str  = None
    
    return result

if __name__ == "__main__":
    app.run(debug=True)