from pprint import pprint

import tkinter as tk
import customtkinter as ctk


class IntInput(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        self.var = ctk.StringVar()
        ctk.CTkEntry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        if self.get().isdigit() or self.get() == "":
            # the current value is only digits; allow this
            self.old_value = self.get()
        else:
            # there's non-digit characters in the input; reject this
            self.set(self.old_value)