import tkinter as tk
from tkinter import ttk


class SaveWindow(object):

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        windowWidth = 240
        windowHeight = 100
        screenWidth = parent.winfo_screenwidth()
        screenHeight = parent.winfo_screenheight()
        center_x = int(screenWidth / 2 - windowWidth / 2)
        center_y = int(screenHeight / 2 - windowHeight / 2)

        top.title("Speichern")
        top.geometry(f'{windowWidth}x{windowHeight}+{center_x}+{center_y}')
        top.iconbitmap('../assets/logo.ico')

        self.label = ttk.Label(top, text="Bitte geben sie einen Dateinamen ein:")
        self.label.pack(anchor="w", padx=10)
        self.entry = ttk.Entry(top)
        self.entry.pack(anchor="w", fill="x", padx=10)
        self.entry.focus()
        self.okBut = ttk.Button(top, text='Ok', command=self.enterValue)
        self.cancelBut = ttk.Button(top, text='Abbrechen', command=self.top.destroy)
        self.okBut.pack(side="left", fill="x", padx=20)
        self.cancelBut.pack(side="right", fill="x", padx=20)

        self.fileName = ""

    def enterValue(self):
        self.fileName = self.entry.get()
        self.top.destroy()
