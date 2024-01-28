import customtkinter as ctk
import tkinter as tk
from tkinter import StringVar, TOP, messagebox, W, E, END
from tkinterdnd2 import TkinterDnD, DND_ALL
from pprint import pprint

from classes.Dummy import Dummy
from classes.LabelledSlider import LabelledSlider
from classes.AppFrame import AppFrame


class App(ctk.CTk):
    def __init__(self, activeSettings):
        super().__init__()

        self.title("Palworld Configuration Tool")

        self.frame = AppFrame(master=self, activeSettingsToUse=activeSettings, width=550, height=700)
        self.frame.grid(row=0, column=0, sticky='nsew')


with open('AvailableSettings.txt') as f:
    activeSettings = [i.strip() for i in f.readlines()]

app = App(activeSettings=activeSettings)
app.mainloop()
