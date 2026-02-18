import json
import main
import os

def startShift():
    if os.path.exists("shiftdata.json"):
        with open("shiftdata.json", "r") as file:
            data = json.load(file)
            data["ClockedIn"] = "Yes"
            with open("shiftdata.json", "w") as file:
                json.dump(data, file)
    else:
        print("Error occurred. Trying again...")
        with open("shiftdata.json", "w") as file:
            json.dump({"ClockedIn": "Yes"}, file)

def endShift():
    if os.path.exists("shiftdata.json"):
        with open("shiftdata.json", "r") as file:
            data = json.load(file)
            data["ClockedIn"] = "No"
            with open("shiftdata.json", "w") as file:
                json.dump(data, file)
    else:
        print("Error occurred. Trying again...")
        with open("shiftdata.json", "w") as file:
            json.dump({"ClockedIn": "No"}, file)

def checkShift():
    if os.path.exists("shiftdata.json"):
        with open("shiftdata.json", "r") as file:
            data = json.load(file)
            if data["ClockedIn"] == "No":
                main.clockIn()
            else:
                main.clockOut()
    else:
        print("Error occurred. Trying again...")
        with open("shiftdata.json", "w") as file:
            json.dump({"ClockedIn": "No"}, file)