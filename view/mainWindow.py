import tkinter as tk
from tkinter import ttk


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
        self.iconbitmap('./assets/logo.ico')

        # add a scrollbar to the window
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollableFrame = ttk.Frame(canvas)
        self.scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.weekdayFrames = {}
        self.therapistEntryField = {}
        self.therapistAddButton = {}
        self.usedRows = {}

    def addWeekday(self, day):
        s = ttk.Style()
        s.configure('Bold.TLabel', font=('TkDefaultFont', 14))
        label = ttk.Label(text=day, style="Bold.TLabel")
        self.weekdayFrames[day] = ttk.LabelFrame(self.scrollableFrame, labelwidget=label)
        self.weekdayFrames[day].columnconfigure(0, weight=1)
        self.weekdayFrames[day].columnconfigure(1, weight=8)
        self.usedRows[day] = 0

        self.addRoom(1, day)
        self.addRoom(2, day)
        self.addRoom(3, day)
        self.addRoom(4, day)

        newTherapistName = tk.StringVar()
        self.therapistEntryField[day] = ttk.Entry(self.weekdayFrames[day], textvariable=newTherapistName)
        self.therapistEntryField[day].grid(column=1, row=self.usedRows[day], sticky=tk.W)

        self.therapistAddButton[day] = ttk.Button(self.weekdayFrames[day], text="+", command=lambda: self.addTherapist(newTherapistName.get(), day))
        self.therapistAddButton[day].grid(column=0, row=self.usedRows[day])
        self.usedRows[day] += 1

        self.weekdayFrames[day].pack(anchor="w", ipadx=10, ipady=5, padx=10, pady=0, side="top")




    def addRoom(self, roomNumber, day):
        roomNameLabel = ttk.Label(self.weekdayFrames[day], text=f"Raum {roomNumber}")
        roomNameLabel.grid(column=0, row=self.usedRows[day])

        occupancyLabel = tk.Label(self.weekdayFrames[day], bg="green", borderwidth=2, relief="sunken", pady=2)
        occupancyLabel.grid(column=1, row=self.usedRows[day], sticky=tk.W, ipadx=850)
        self.usedRows[day] += 1


    def addTherapist(self, name, weekday):
        if name == "":
            return

        print(f"Add Therapist {name}!")
        ttk.Label(self.weekdayFrames[weekday], text=name).grid(column=0, row=self.usedRows[weekday]-1)
        self.therapistEntryField[weekday].grid(column=1, row=self.usedRows[weekday], sticky=tk.W)
        self.therapistAddButton[weekday].grid(column=0, row=self.usedRows[weekday])
        self.usedRows[weekday] += 1
