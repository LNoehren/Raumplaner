import tkinter as tk
from tkinter import ttk
import view.resizingCanvas


class MainWindow(tk.Tk):

    windowWidth = 1920
    windowHeight = 1080

    def __init__(self, addTherapistCallback):
        super().__init__()

        self.addTherapistCallback = addTherapistCallback

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
        self.iconbitmap('./assets/logo.ico')

        # add a scrollbar to the window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)
        canvas = view.resizingCanvas.ResizingCanvas(self, height=self.windowHeight, width=self.windowWidth)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.grid(column=0, row=0, sticky="news")
        scrollbar.grid(column=1, row=0, sticky="news")
        self.scrollableFrame = ttk.Frame(canvas)
        self.scrollableFrame.columnconfigure(0, weight=1)
        self.scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw", height=self.windowHeight, width=self.windowWidth-10)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.addtag_all("all")

        self.weekdayFrames = {}
        self.therapistEntryField = {}
        self.therapistAddButton = {}
        self.usedRows = {}

    def addWeekday(self, day, numberOfRooms):
        s = ttk.Style()
        s.configure('Bold.TLabel', font=('TkDefaultFont', 14))
        label = ttk.Label(text=day, style="Bold.TLabel")
        self.weekdayFrames[day] = ttk.LabelFrame(self.scrollableFrame, labelwidget=label)
        self.weekdayFrames[day].columnconfigure(0, weight=0)
        self.weekdayFrames[day].columnconfigure(1, weight=1)
        self.usedRows[day] = 0

        for i in range(numberOfRooms):
            self.addRoom(i+1, day)

        newTherapistName = tk.StringVar()
        self.therapistEntryField[day] = ttk.Entry(self.weekdayFrames[day], textvariable=newTherapistName)
        self.therapistEntryField[day].grid(column=1, row=self.usedRows[day], sticky="w")

        self.therapistAddButton[day] = ttk.Button(self.weekdayFrames[day], text="+", command=lambda: self.addTherapist(newTherapistName.get(), day))
        self.therapistAddButton[day].grid(column=0, row=self.usedRows[day], sticky="w")
        self.usedRows[day] += 1

        self.weekdayFrames[day].grid(row=len(self.weekdayFrames)-1, ipadx=10, ipady=5, padx=10, pady=0, sticky="ew")

    def addRoom(self, roomNumber, day):
        roomNameLabel = ttk.Label(self.weekdayFrames[day], text=f"Raum {roomNumber}")
        roomNameLabel.grid(column=0, row=self.usedRows[day])

        # hier kann man vielleicht canvas.create_rectangle nutzen, vielleicht dann sowas wie activefill='blue' nutzen
        canvas = tk.Canvas(self.weekdayFrames[day])
        #canvas.grid(column=1, row=self.usedRows[day], sticky=tk.W, ipadx=850)
        canvasX = canvas.winfo_x()
        canvasY = canvas.winfo_y()
        canvasWidth = canvas.winfo_width()
        canvasHeight = canvas.winfo_height()
        #canvas.create_rectangle(canvasX, canvasY, canvasX + canvasWidth, canvasY + canvasHeight, fill="green")
        occupancyLabel = tk.Label(self.weekdayFrames[day], bg="green", borderwidth=2, relief="sunken", pady=2)
        occupancyLabel.grid(column=1, row=self.usedRows[day], sticky="ew")
        self.usedRows[day] += 1

    def addTherapist(self, name, weekday):
        if name == "":
            return

        print(f"Adding Therapist {name}!")
        ttk.Label(self.weekdayFrames[weekday], text=name).grid(column=0, row=self.usedRows[weekday]-1)
        self.therapistEntryField[weekday].grid(column=1, row=self.usedRows[weekday], sticky=tk.W)
        self.therapistAddButton[weekday].grid(column=0, row=self.usedRows[weekday])
        self.usedRows[weekday] += 1

        remainingTimeSlots = self.addTherapistCallback(weekday, name, 480, 960)  # TODO start and end times

        if len(remainingTimeSlots) > 0:
            print(remainingTimeSlots)
