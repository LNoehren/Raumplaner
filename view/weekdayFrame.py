import tkinter as tk
from tkinter import ttk

import utils
import view.resizingCanvas
import view.timeOccupancyCanvas


class WeekdayFrame(ttk.LabelFrame):

    possibleTherapistColors = ["#512E5F", "#4A235A", "#154360", "#1B4F72", "#0E6251", "#0B5345", "#145A32", "#186A3B",
                               "#7D6608", "#7E5109", "#784212", "#6E2C00", "#1B2631", "#17202A"]

    def __init__(self, parent, day, roomList, addTherapistCallback, **kwargs):
        super().__init__(parent, **kwargs)

        self.day = day
        self.rooms = roomList
        self.addTherapistCallback = addTherapistCallback

        self.roomWidgets = {}
        self.therapistData = {}

        s = ttk.Style()
        s.configure('Bold.TLabel', font=('TkDefaultFont', 14))
        label = ttk.Label(text=day, style="Bold.TLabel")
        self.configure(labelwidget=label)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=0)

        self.usedRows = 0

        timeCanvas = view.resizingCanvas.ResizingCanvas(self, height=22)
        timeCanvas.grid(column=1, row=self.usedRows, sticky="ew")
        self.usedRows += 1

        for room in self.rooms:
            self.addRoom(room)

        referenceRoomWidget = self.roomWidgets[self.rooms[0].id]
        for i in range(0, len(self.rooms[0].occupation), 1):
            rectPos = referenceRoomWidget.coords(referenceRoomWidget.timeSlots[i])
            rectPos[0] += 5 if i == 0 else 2
            timeValue = self.rooms[0].computeTimeFromOccupationIndex(i)
            timeCanvas.create_text(rectPos[0], 14, text=utils.timeToTimeString(timeValue), angle=35)

        self.separatorLeft = ttk.Separator(self, orient="horizontal")
        self.separatorLeft.grid(column=0, row=self.usedRows, sticky="ew", pady=5)
        self.separatorRight = ttk.Separator(self, orient="horizontal")
        self.separatorRight.grid(column=1, row=self.usedRows, sticky="ew", pady=5)
        self.usedRows += 1

        newTherapistName = tk.StringVar()
        self.therapistEntryField = ttk.Entry(self, textvariable=newTherapistName)
        self.therapistEntryField.grid(column=1, row=self.usedRows, sticky="w")
        self.therapistEntryField.bind("<Return>", lambda event: self.addTherapist(newTherapistName.get()))

        self.therapistAddButton = ttk.Button(self, text="+", command=lambda: self.addTherapist(newTherapistName.get()))
        self.therapistAddButton.grid(column=0, row=self.usedRows, sticky="w")
        self.usedRows += 1

    def addRoom(self, room):
        roomNameLabel = ttk.Label(self, text=f"Raum {room.id}")
        roomNameLabel.grid(column=0, row=self.usedRows)

        canvas = view.timeOccupancyCanvas.TimeOccupancyCanvas(self, len(room.occupation), True,
                                                              height=12, bg="grey", borderwidth=2, relief="sunken")
        canvas.grid(column=1, row=self.usedRows, sticky="ew")

        self.usedRows += 1
        self.roomWidgets[room.id] = canvas

    def addTherapist(self, name):
        if name == "" or name in self.therapistData:
            return

        curTherapistData = {}
        curTherapistData["label"] = ttk.Label(self, text=name)
        curTherapistData["label"].grid(column=0, row=self.usedRows)

        curTherapistData["colorVar"] = tk.StringVar(self, WeekdayFrame.possibleTherapistColors[0])
        curTherapistData["colorMenu"] = ttk.OptionMenu(self, curTherapistData["colorVar"], *WeekdayFrame.possibleTherapistColors)
        curTherapistData["colorMenu"].grid(column=2, row=self.usedRows)

        curTherapistData["canvas"] = view.timeOccupancyCanvas.TimeOccupancyCanvas(self, len(self.rooms[0].occupation), False, activeColor=curTherapistData["colorVar"].get(), height=12,
                                                              bg=view.timeOccupancyCanvas.INACTIVE_THERAPIST_COLOR, borderwidth=2, relief="sunken")
        curTherapistData["canvas"].grid(column=1, row=self.usedRows, sticky="ew")

        curTherapistData["removeBtn"] = ttk.Button(self, text="-", command=lambda: self.removeTherapist(name))
        curTherapistData["removeBtn"].grid(column=3, row=self.usedRows)

        self.usedRows += 1
        self.moveTherapistEntryRow()
        self.therapistEntryField.delete(0, "end")

        therapistTimeCallback = self.addTherapistCallback(self.day, name)
        curTherapistData["canvas"].setTherapistTimes = therapistTimeCallback

        self.therapistData[name] = curTherapistData
        curTherapistData["colorVar"].trace("w", lambda a, b, c: self.updateTherapistColor(name))

    def updateTherapistColor(self, name):
        self.therapistData[name]["canvas"].changeActiveColor(self.therapistData[name]["colorVar"].get())

    def removeTherapist(self, name):
        self.addTherapistCallback(self.day, name, delete=True)

        usedRow = self.therapistData[name]["label"].grid_info()["row"]
        self.therapistData[name]["label"].destroy()
        self.therapistData[name]["canvas"].destroy()
        self.therapistData[name]["colorMenu"].destroy()
        self.therapistData[name]["removeBtn"].destroy()
        del self.therapistData[name]

        self.moveLowerTherapistsUp(usedRow+1)
        self.usedRows -= 1
        self.moveTherapistEntryRow()

    def moveLowerTherapistsUp(self, beginRow):
        for therapistName in self.therapistData:
            oldRow = self.therapistData[therapistName]["label"].grid_info()["row"]
            if oldRow >= beginRow:
                self.therapistData[therapistName]["label"].grid(column=0, row=oldRow-1)
                self.therapistData[therapistName]["canvas"].grid(column=1, row=oldRow-1, sticky="ew")
                self.therapistData[therapistName]["colorMenu"].grid(column=2, row=oldRow-1)
                self.therapistData[therapistName]["removeBtn"].grid(column=3, row=oldRow-1)

    def moveTherapistEntryRow(self):
        self.therapistEntryField.grid(column=1, row=self.usedRows, sticky=tk.W)
        self.therapistAddButton.grid(column=0, row=self.usedRows)

    def setRoomOccupation(self, roomName, occupationSlot, isOccupied):
        if isOccupied:
            self.roomWidgets[roomName].setSlotColors([occupationSlot], view.timeOccupancyCanvas.OCCUPIED_ROOM_COLOR)
        else:
            self.roomWidgets[roomName].setSlotColors([occupationSlot], view.timeOccupancyCanvas.FREE_ROOM_COLOR)

    def setTherapistAssignment(self, therapistName, occupationSlot, wasAssigned):
        if wasAssigned:
            self.therapistData[therapistName]["canvas"].setSlotColors(occupationSlot, self.therapistData[therapistName]["colorVar"].get())
        else:
            self.therapistData[therapistName]["canvas"].setSlotColors(occupationSlot, view.timeOccupancyCanvas.OCCUPIED_ROOM_COLOR)