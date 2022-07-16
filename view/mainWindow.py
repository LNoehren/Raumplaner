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

        # find the center point
        center_x = int(screenWidth / 2 - self.windowWidth / 2)
        center_y = int(screenHeight / 2 - self.windowHeight / 2)

        self.geometry(f'{self.windowWidth}x{self.windowHeight}+{center_x}+{center_y}')

        # window.minsize(min_width, min_height)
        # window.maxsize(min_height, max_height)
        self.iconbitmap('../assets/logo.ico')

        # add a scrollbar to the window
        # TODO funktioniert nicht richtig mit dem ResizingCanvas. Entweder funktioniert die scrollbar, oder das resizing...
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)
        self.mainCanvas = view.resizingCanvas.ResizingCanvas(self, height=self.windowHeight, width=self.windowWidth, resizeHeight=True)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.mainCanvas.yview)
        self.mainCanvas.grid(column=0, row=0, sticky="news")
        scrollbar.grid(column=1, row=0, sticky="news")
        self.scrollableFrame = ttk.Frame(self.mainCanvas)
        self.scrollableFrame.columnconfigure(0, weight=1)
        self.scrollableFrame.bind("<Configure>", lambda e: self.mainCanvas.configure(scrollregion=(0, 0, 0, self.windowHeight)))
        #self.scrollableFrame.bind("<Configure>", lambda e: self.mainCanvas.configure(scrollregion=self.mainCanvas.bbox("all")))
        self.mainCanvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw", height=self.windowHeight, width=self.windowWidth-10)
        self.mainCanvas.configure(yscrollcommand=scrollbar.set)
        self.mainCanvas.addtag_all("all")
        # TODO muss hier noch das <MouseWheel> irgendwie binden!

        self.weekdayFrames = {}

    def addWeekday(self, day, roomList, addTherapistCallback):
        self.weekdayFrames[day] = view.weekdayFrame.WeekdayFrame(self.scrollableFrame, day, roomList,
                                                                 addTherapistCallback)
        self.weekdayFrames[day].grid(row=len(self.weekdayFrames)-1, ipadx=10, ipady=5, padx=10, pady=0, sticky="ew")

    def addRoom(self, day, roomName):
        self.weekdayFrames[day].addRoom(roomName)

    def setRoomOccupation(self, day, room, occupationSlot, isOccupied):
        self.weekdayFrames[day].setRoomOccupation(room, occupationSlot, isOccupied)

    def setTherapistAssignment(self, day, therapistName, occupationSlot, wasAssigned):
        self.weekdayFrames[day].setTherapistAssignment(therapistName, occupationSlot, wasAssigned)
