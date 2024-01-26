import customtkinter as ctk
import tkinter as tk
from tkinter import StringVar, TOP, messagebox, W, E, END
from tkinterdnd2 import TkinterDnD, DND_ALL
from pprint import pprint

from classes.Dummy import Dummy
from classes.LabelledSlider import LabelledSlider


class App(ctk.CTk):
    def __init__(self, activeSettings):
        super().__init__()

        self.title("Palworld Configuration Tool")

        self.frame = Frame(master=self, activeSettingsToUse=activeSettings, width=550, height=700)
        self.frame.grid(row=0, column=0, sticky='nsew')


class Frame(ctk.CTkScrollableFrame, TkinterDnD.DnDWrapper):
    settings = {}
    currentRow = 0
    settingsRowStart = 0
    activeSettings = []
    hasFileLoaded = False

    def __init__(self, master, **kwargs):
        self.activeSettings = kwargs['activeSettingsToUse']

        del kwargs['activeSettingsToUse']

        super().__init__(master, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

        # self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1, pad=5)
        self.grid_columnconfigure(1, weight=2, pad=5)
        # self.grid_rowconfigure((0, 1), weight=1, pad=50)

        self.entryWidget = ctk.CTkEntry(self, width=350)
        # self.entryWidget.pack(side=TOP, padx=5, pady=5)
        self.entryWidget.grid(row=self.useRow(), column=0)
        self.entryWidget.drop_target_register(DND_ALL)
        self.entryWidget.dnd_bind("<<Drop>>", self.getPath)
        self.entryWidget.configure(state='disabled')

        self.pathLabel = ctk.CTkLabel(self, text="Drag and drop the PalWorldSettings.ini file into the above box:")
        self.pathLabel.grid(row=self.useRow(), column=0, columnspan=2, sticky=W+E)
        # self.pathLabel.pack(side=TOP)

        self.inputs = {}
        self.saveBtn = None
        self.settingsRowStart = self.currentRow

    def useRow(self):
        row = self.currentRow
        self.currentRow += 1

        self.grid_rowconfigure(row, weight=row, pad=1)

        return row

    def addSettings(self):
        for setting in self.settings.keys():
            data = self.settings[setting]

            print(setting)

            if setting not in self.activeSettings:
                self.inputs[setting] = Dummy(data['value'])
                print(setting, 'dummy!')
                continue

            if data['type'] == 'text':
                row = self.useRow()

                label = ctk.CTkLabel(self, text=setting)
                label.grid(row=row, column=0)

                inp = ctk.CTkEntry(self, placeholder_text="Hi!", width=350)
                inp.insert(0, data['value'])
                inp.grid(row=row, column=1)
                self.inputs[setting] = inp

            elif data['type'] == 'dropdown':
                row = self.useRow()

                label = ctk.CTkLabel(self, text=setting)
                label.grid(row=row, column=0)

                inp = ctk.CTkOptionMenu(self, values=data['options'])
                inp.set(data['value'])
                inp.grid(row=row, column=1)
                self.inputs[setting] = inp

            elif data['type'] == 'percentage':
                row = self.useRow()

                label = ctk.CTkLabel(self, text=setting)
                label.grid(row=row, column=0)

                inp = LabelledSlider(self, from_=0, to=5, value=data['value'])
                inp.grid(row=row, column=1)
                self.inputs[setting] = inp

            elif data['type'] == 'bool':
                row = self.useRow()

                label = ctk.CTkLabel(self, text=setting)
                label.grid(row=row, column=0)

                inp = ctk.CTkCheckBox(self, text='')
                inp.grid(row=row, column=1)
                self.inputs[setting] = inp

            # elif data['type'] == 'number':
            #     row = self.useRow()
            #
            #     label = ctk.CTkLabel(self, text=setting)
            #     label.grid(row=row, column=0)
            #
            #     inp = LabelledSlider(self, from_=0, to=5, value=data['value'])
            #     inp.grid(row=row, column=1)
            #     self.inputs[setting] = inp

        self.saveBtn = ctk.CTkButton(self, text="Save", command=self.save)
        self.saveBtn.grid(row=self.useRow(), column=1)

    def getPath(self, event):
        self.entryWidget.insert(0, event.data)
        self.entryWidget.xview_moveto(len(event.data))
        self.loadFile(event.data)

    def save(self):
        print('saving')
        with open('config.ini', 'w') as f:
            f.write('[/Script/Pal.PalGameWorldSettings]\n')
            f.write('OptionSettings=(')

            # Write configs
            for setting in self.settings:
                sConfig = self.settings[setting]
                value = self.inputs[setting].get()

                print(setting, value)

                f.write(f'{setting}=')

                if sConfig['type'] == 'percentage':
                    f.write('{:10.6f}'.format(value).strip())
                else:
                    f.write(f'{value}')

                f.write(',')

            f.write(')')

        messagebox.showinfo('Config Save', f'Saved successfully to: {self.entryWidget.get()}')

    def loadFile(self, path):
        with open(path) as f:
            lines = f.readlines()

        if len(lines) != 2:
            messagebox.showerror(
                'Error Reading Settings File',
                'Settings file should have 2 lines in it. One starting with ' +
                '"[/Script/Pal.PalGameWorldSettings]" and one starting with "OptionSettings=("'
            )
            return

        settings = [
            item.split('=')
            for item in
            lines[1][16:-1].split(',')
        ]

        for i, item in enumerate(settings):
            name = item[0]
            value = item[1]

            res = {
                'order': i,
                'type': '',
                'value': '',
                'name': name,
            }

            if name == 'DeathPenalty':
                res['type'] = 'dropdown'
                res['value'] = value
                res['options'] = ('None', 'Item', 'ItemAndEquipment', 'All')
            elif name == 'Difficulty':
                res['type'] = 'dropdown'
                res['value'] = value
                res['options'] = ('None',)
            elif 'Rate' in name:
                res['type'] = 'percentage'
                res['value'] = float(value)
            elif value in ('True', 'False'):
                res['type'] = 'bool'
                res['value'] = value == 'True'
            elif 'Time' in name or 'MaxNum' in name or 'MaxHours' in name or 'Port' in name:
                res['type'] = 'number'
                res['value'] = int(value.split('.')[0])
            else:
                res['type'] = 'text'
                res['value'] = value[1:-1]

            self.settings[name] = res

        self.addSettings()


activeSettings = [
    'Difficulty',
    'DayTimeSpeedRate',
    'NightTimeSpeedRate',
    'ExpRate',
    'PalCaptureRate',
    'PalSpawnNumRate',
    'PalDamageRateAttack',
    'PalDamageRateDefense',
    'PlayerDamageRateAttack',
    'PlayerDamageRateDefense',
    'PlayerStomachDecreaceRate',
    'PlayerStaminaDecreaceRate',
    'PlayerAutoHPRegeneRate',
    'PlayerAutoHpRegeneRateInSleep',
    'PalStomachDecreaceRate',
    'PalStaminaDecreaceRate',
    'PalAutoHPRegeneRate',
    'PalAutoHpRegeneRateInSleep',
    'BuildObjectDamageRate',
    'BuildObjectDeteriorationDamageRate',
    'CollectionDropRate',
    'CollectionObjectHpRate',
    'CollectionObjectRespawnSpeedRate',
    'EnemyDropItemRate',
    'DeathPenalty',
    'GuildPlayerMaxNum',
    'PalEggDefaultHatchingTime',
    'ServerPlayerMaxNum',
    'ServerName',
    'ServerDescription',
    'AdminPassword',
    'ServerPassword',
    'PublicPort',
    'PublicIP',
    'RCONEnabled',
    'RCONPort',
]

app = App(activeSettings=activeSettings)
app.mainloop()
