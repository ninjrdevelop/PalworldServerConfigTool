from pprint import pprint

import customtkinter as ctk


class LabelledSlider(ctk.CTkFrame):
    prefix = ''
    suffix = ''
    isPercentage = False

    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.suffix = kwargs['suffix'] if 'suffix' in kwargs else ''
        self.prefix = kwargs['prefix'] if 'prefix' in kwargs else ''
        self.isPercentage = kwargs['isPercentage'] if 'isPercentage' in kwargs else ''

        #
        self.label = ctk.CTkLabel(self, text=self.fmt(kwargs['value']))
        self.label.pack()

        #
        self.slider = ctk.CTkSlider(self,
                                    from_=kwargs['from_'],
                                    to=kwargs['to'],
                                    command=self._sliderChange)
        self.slider.set(kwargs['value'])
        self.slider.pack()

    def _sliderChange(self, value):
        self.label.configure(text=self.fmt(value))

    def get(self):
        if self.isPercentage:
            return int(self.slider.get() * 100) / 100
        else:
            return self.slider.get()

    def fmt(self, value):
        if self.isPercentage:
            return f'{self.prefix}{int(value * 100)}{self.suffix}'
        else:
            return f'{self.prefix}{value}{self.suffix}'
