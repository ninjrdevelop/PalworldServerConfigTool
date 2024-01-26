from pprint import pprint

import customtkinter as ctk


class LabelledSlider(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        #
        self.label = ctk.CTkLabel(self, text=fmt(kwargs['value']))
        self.label.pack()

        #
        self.slider = ctk.CTkSlider(self,
                                    from_=kwargs['from_'],
                                    to=kwargs['to'],
                                    command=self._sliderChange)
        self.slider.set(kwargs['value'])
        self.slider.pack()

    def _sliderChange(self, value):
        self.label.configure(text=fmt(value))

        print(self.get())

    def get(self):
        return int(self.slider.get() * 100) / 100


def fmt(value):
    return f'{int(value * 100)} %'
