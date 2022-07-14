import tkinter as tk
from tkinter import ttk
import view.timeOccupancyCanvas


class WeekdayFrame(ttk.LabelFrame):

    def __init__(self, parent, day, nrTimeSlots, addTherapistCallback, **kwargs):
        super().__init__(parent, **kwargs)

        self.day = day
        self.nrTimeSlots = nrTimeSlots
        self.addTherapistCallback = addTherapistCallback

        s = ttk.Style()
        s.configure('Bold.TLabel', font=('TkDefaultFont', 14))
        label = ttk.Label(text=day, style="Bold.TLabel")
        self.configure(labelwidget=label)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.usedRows = 0

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

    def addRoom(self, roomName):
        roomNameLabel = ttk.Label(self, text=f"Raum {roomName}")
        roomNameLabel.grid(column=0, row=self.usedRows)

        canvas = view.timeOccupancyCanvas.TimeOccupancyCanvas(self, self.nrTimeSlots, True, height=12, bg="grey",
                                                              borderwidth=2, relief="sunken")
        canvas.grid(column=1, row=self.usedRows, sticky="ew")

        self.usedRows += 1
        self.separatorLeft.grid(column=0, row=self.usedRows, sticky="ew", pady=5)
        self.separatorRight.grid(column=1, row=self.usedRows, sticky="ew", pady=5)
        self.usedRows += 1
        self.moveTherapistEntryRow()

    def addTherapist(self, name):
        if name == "":
            return

        print(f"Adding Therapist {name}!")
        ttk.Label(self, text=name).grid(column=0, row=self.usedRows)

        canvas = view.timeOccupancyCanvas.TimeOccupancyCanvas(self, self.nrTimeSlots, False, height=12, bg="grey",
                                                              borderwidth=2, relief="sunken")
        canvas.grid(column=1, row=self.usedRows, sticky="ew")

        self.usedRows += 1
        self.moveTherapistEntryRow()
        self.therapistEntryField.delete(0, "end")

        remainingTimeSlots = self.addTherapistCallback(self.day, name, 480, 960)  # TODO start and end times

        if len(remainingTimeSlots) > 0:
            print(remainingTimeSlots)

    def moveTherapistEntryRow(self):
        self.therapistEntryField.grid(column=1, row=self.usedRows, sticky=tk.W)
        self.therapistAddButton.grid(column=0, row=self.usedRows)
