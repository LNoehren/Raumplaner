import json


class Configuration:

    def __init__(self):
        self.numberOfRooms = 4
        self.minimalTimeSlot = 20
        self.openingTime = {"Montag": "08:00",
                            "Dienstag": "08:00",
                            "Mittwoch": "08:00",
                            "Donnerstag": "08:00",
                            "Freitag": "08:00"}
        self.closingTime = {"Montag": "19:00",
                            "Dienstag": "19:00",
                            "Mittwoch": "19:00",
                            "Donnerstag": "19:00",
                            "Freitag": "16:00"}

    def read(self, filepath):
        with open(filepath, "r") as file:
            data = json.load(file)

            if "numberOfRooms" in data:
                self.numberOfRooms = data["numberOfRooms"]

            if "minimalTimeSlot" in data:
                self.minimalTimeSlot = data["minimalTimeSlot"]

            if "openingTime" in data:
                self.openingTime = data["openingTime"]

            if "closingTime" in data:
                self.closingTime = data["closingTime"]
