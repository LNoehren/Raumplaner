import tkinter as tk
from tkinter import ttk

import utils
import view.resizingCanvas
import view.timeOccupancyCanvas


class WeekdayFrame(ttk.LabelFrame):

    def __init__(self, parent, day, roomList, addTherapistCallback, **kwargs):
        super().__init__(parent, **kwargs)

        self.day = day
        self.rooms = roomList
        self.addTherapistCallback = addTherapistCallback

        self.roomWidgets = {}
        self.therapists = {}

        s = ttk.Style()
        s.configure('Bold.TLabel', font=('TkDefaultFont', 14))
        label = ttk.Label(text=day, style="Bold.TLabel")
        self.configure(labelwidget=label)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

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
        if name == "":
            return

        ttk.Label(self, text=name).grid(column=0, row=self.usedRows)

        canvas = view.timeOccupancyCanvas.TimeOccupancyCanvas(self, len(self.rooms[0].occupation), False, height=12,
                                                              bg=view.timeOccupancyCanvas.INACTIVE_THERAPIST_COLOR,
                                                              borderwidth=2, relief="sunken")
        canvas.grid(column=1, row=self.usedRows, sticky="ew")

        self.usedRows += 1
        self.moveTherapistEntryRow()
        self.therapistEntryField.delete(0, "end")

        therapistTimeCallback = self.addTherapistCallback(self.day, name)
        canvas.setTherapistTimes = therapistTimeCallback

        self.therapists[name] = canvas

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
            self.therapists[therapistName].setSlotColors(occupationSlot, view.timeOccupancyCanvas.ACTIVE_THERAPIST_COLOR)
        else:
            self.therapists[therapistName].setSlotColors(occupationSlot, view.timeOccupancyCanvas.OCCUPIED_ROOM_COLOR)