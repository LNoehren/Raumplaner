import tkinter as tk
from tkinter import ttk
import view.resizingCanvas
import view.weekdayFrame


class MainWindow(tk.Tk):

    windowWidth = 1920
    windowHeight = 1080

    def __init__(self):
        super().__init__()

        self.title("Raumplaner")

        # get the screen dimension
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        self.windowWidth = int(screenWidth/2)
        self.windowHeight = int(screenHeight/2)

        # find the center point
        center_x = int(screenWidth / 2 - self.windowWidth / 2)
        center_y = int(screenHeight / 2 - self.windowHeight / 2)

        self.geometry(f'{self.windowWidth}x{self.windowHeight}+{center_x}+{center_y}')

        self.iconbitmap('../assets/logo.ico')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(anchor="n", fill="both")
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)

        self.weekdayFrames = {}

    def addWeekday(self, day, roomList, addTherapistCallback):
        self.weekdayFrames[day] = view.weekdayFrame.WeekdayFrame(self.notebook, day, roomList, addTherapistCallback)
        self.weekdayFrames[day].grid(sticky="ew")
        self.notebook.add(child=self.weekdayFrames[day], text=day)

    def addRoom(self, day, roomName):
        self.weekdayFrames[day].addRoom(roomName)

    def setRoomOccupation(self, day, room, occupationSlot, therapistName):
        occupationSlot += 1  # IDs in the UI are increased by 1 compared to controller...
        self.weekdayFrames[day].setRoomOccupation(room, occupationSlot, therapistName)

    def setTherapistAssignment(self, day, therapistName, occupationSlotList, wasAssigned):
        occupationSlotList = [slot + 1 for slot in occupationSlotList]  # IDs in the UI are increased by 1 compared to controller...
        self.weekdayFrames[day].setTherapistAssignment(therapistName, occupationSlotList, wasAssigned)
