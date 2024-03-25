import tkinter as tk
from tkinter import ttk
from utilities import FileData
from datetime import datetime, date

class BMIWindow(tk.Toplevel):
    def __init__(self, master=None, person_instance=None, nick=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.geometry('1000x500')
        self.resizable(False, False)
        self.title('BMI')
        self.person_instance = person_instance
        self.person_instance.bmi
        self.nick = nick
        self.data_instance = FileData(self.nick, self.person_instance)
        self.welcome_label = self.create_welcome_label()
        self.bmi_label = ttk.Label(
                self,
                text=f'Your BMI equals:\n{self.person_instance.bmi:.2f}\n'
                     f'You are {self.person_instance.bmi_classification()}',
                font=('Corbel', 16, 'bold'),
                justify='center',
                foreground=self.choose_color()
            )

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        self.welcome_label.grid(row=0, column=1, columnspan=2, sticky='nsew')
        self.bmi_label.grid(row=1, column=0, sticky='nsew')

    def count_days(self):
        return date.today() - self.data_instance.get_last_date()

    def create_welcome_label(self):
        if self.data_instance.isuserfile():
            return ttk.Label(
                self,
                text=f'Hello {self.nick} !\n It was {str(self.count_days()).split(',')[0]} since your last visit !',
                font=('Corbel', 16, 'bold'),
            )
        else:
            return ttk.Label(
                self,
                text=f'Hello {self.nick} !\n It\'s your first use of this application !',
                justify='center',
                font=('Corbel', 16, 'bold')
            )

    def choose_color(self):
        if self.person_instance.bmi_classification() == 'Underweight':
            return 'yellow'
        elif self.person_instance.bmi_classification() == 'Normal':
            return 'green'
        elif self.person_instance.bmi_classification() == 'Overweight':
            return 'orange'
        else:
            return 'red'
