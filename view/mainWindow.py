import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox

import view.resizingCanvas
import view.weekdayFrame
import view.savePopup


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

        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Speichern", command=self.saveData)
        file_menu.add_command(label="Laden", command=self.loadData)
        file_menu.add_separator()
        file_menu.add_command(label='Beenden', command=self.destroy)
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(anchor="n", fill="both")
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)

        self.weekdayFrames = {}

        self.saveCallback = None
        self.loadCallback = None

    def addWeekday(self, day, roomList, addTherapistCallback):
        self.weekdayFrames[day] = view.weekdayFrame.WeekdayFrame(self.notebook, day, roomList, addTherapistCallback)
        self.weekdayFrames[day].grid(sticky="ew" )
        self.notebook.add(child=self.weekdayFrames[day], text=day)

    def addRoom(self, day, roomName):
        self.weekdayFrames[day].addRoom(roomName)

    def addTherapist(self, day, name, setTimeCallback):
        self.weekdayFrames[day].addTherapist(name, setTimeCallback)

    def setRoomOccupation(self, day, room, occupationSlot, therapistName):
        occupationSlot += 1  # IDs in the UI are increased by 1 compared to controller...
        self.weekdayFrames[day].setRoomOccupation(room, occupationSlot, therapistName)

    def setTherapistAssignment(self, day, therapistName, occupationSlotList, wasAssigned):
        occupationSlotList = [slot + 1 for slot in occupationSlotList]  # IDs in the UI are increased by 1 compared to controller...
        self.weekdayFrames[day].setTherapistAssignment(therapistName, occupationSlotList, wasAssigned)

    def saveData(self):
        saveDirectory = fd.askdirectory(title="Wählen sie einen Speicherort aus")
        popup = view.savePopup.SaveWindow(self)
        self.wait_window(popup.top)
        fileName = popup.fileName

        success = self.saveCallback(saveDirectory + "/" + fileName + ".plan")

        if not success:
            messagebox.showerror(title="Speichern Fehlgeschlagen",
                                 message="Achtung, speichern is Fehlgeschlagen!\nBitte versuchen sie es erneut.")

    def loadData(self):
        extensions = (("Raumplaner Speicherdatei", "*.plan"), ("Alle Dateitypen", "*.*"))
        fileName = fd.askopenfilename(title="Wählen sie eine Datei aus", filetypes=extensions)

        self.notebook.update()
        for frameId in self.notebook.winfo_children():
            self.notebook.forget(frameId)
        for weekday in self.weekdayFrames:
            self.weekdayFrames[weekday].destroy()

        loadResult = self.loadCallback(fileName)

        if loadResult != "SUCCESS":
            if loadResult == "OLD_VERSION":
                messagebox.showwarning(title="Veraltete Version geladen",
                                       message=f"Achtung, die Datei {fileName} wurde mit einer älteren "
                                               f"Version des Programms erstellt. Es kann nicht garantiert werden, dass "
                                               f"alle Daten korrekt geladen wurden!\n"
                                               f"Bitte überprüfen sie die Daten und erzeugen eine neue Speicherdatei "
                                               f"mit der aktuellen Version um potentielle Fehler zu vermeiden.")
            else:
                messagebox.showerror(title="Laden Fehlgeschlagen",
                                     message="Achtung, laden is Fehlgeschlagen!\n"
                                             f"{fileName} ist keine gültige Datei.\n"
                                             f"Bitte wählen sie eine andere Datei aus.")
