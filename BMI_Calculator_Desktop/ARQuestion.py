import tkinter as tk
from tkinter import ttk

from ValidationSpinbox import ValidationSpinbox
from utilities import Propositions
from MetabolismWindow import MetabolismWindow


class ARQuestion(tk.Toplevel):
    """
    Class ARQuestion inherits from tk.TopLevel and adds specific widgets for specific use inside BMICalculator.
    :param data_instance: takes data_instance created for specific user after login
    :param nick: takes nick variable out of login_instance made for specific user after login
    """

    def __init__(self, master, data_instance, nick, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.data_instance = data_instance
        self.nick = nick
        self.age = None
        self.gender = None
        self.ar = None
        self.propositions_instance = None
        #Creating widgets that will be inside this question window
        self.main_label = ttk.Label(
            self,
            text='To check your energy demand,'
                 '\nYou have to insert Your age, gender and activity rate !',
            font=('Corbel', 16, 'bold'),
            justify='center'
        )
        self.age_lbl = ttk.Label(
            self,
            text='Choose your age !',
            font=('Corbel', 12, 'italic'),
            justify='right'
        )
        self.age_spinbox = ValidationSpinbox(
            self,
            lower_threshold=10,
            values=list(map(lambda x: str(x), range(10, 100)))
        )
        self.gender_lbl = ttk.Label(
            self,
            text='Choose your gender !',
            font=('Corbel', 12, 'italic'),
            justify='right'
        )
        self.gender_combobox = ttk.Combobox(
            self,
            values=['female', 'male'],
            state='readonly'
        )
        self.activity_lbl = ttk.Label(
            self,
            text='Select matching activity rate !',
            font=('Corbel', 12, 'italic'),
            justify='right'
        )
        self.activity_rate = ttk.Combobox(
            self,
            values=[
                '1 - Negligible (no exercise, sedentary work)',
                '2 - Very little (exercise once a week, light work)',
                '3 - Moderate (exercise twice a week at medium intensity)',
                '4 - Heavy (quite heavy training several times a week)',
                '5 - Very high (at least 4 hard training sessions a week, physical work)'
            ],
            state='readonly',
            width=60
        )
        self.confirm_btn = ttk.Button(
            self,
            text='Confirm',
            state='disabled'
        )
        self.confirm_btn.bind('<Button>', self.confirm)

        #Putting the widgets into the window
        self.main_label.grid(row=0, column=0, columnspan=2)
        self.age_lbl.grid(row=1, column=0)
        self.age_spinbox.grid(row=1, column=1, sticky='ew')
        self.gender_lbl.grid(row=2, column=0)
        self.gender_combobox.grid(row=2, column=1, sticky='ew')
        self.activity_lbl.grid(row=3, column=0)
        self.activity_rate.grid(row=3, column=1, sticky='ew')
        self.confirm_btn.grid(row=4, column=1)

    #Defining confirm method used to confirm chosen by user params, and open MetabolismWindow
    def confirm(self, event):
        params_list = [self.__getattribute__(instance).get() for instance in self.__dict__.keys() if
                            isinstance(self.__getattribute__(instance), ValidationSpinbox) or
                            isinstance(self.__getattribute__(instance), ttk.Combobox)]
        if all(params_list):
            self.confirm_btn.config(state='normal')
            self.propositions_instance = Propositions(
                person_instance=self.data_instance.last_record_person_instance(),
                age=int(self.age_spinbox.get()),
                gender=self.gender_combobox.get(),
                activity_rate=self.activity_rate.get(),
            )
            self.metabolism_window = MetabolismWindow(
                self,
                self.propositions_instance,
                self.nick
            )
        else:
            self.confirm_btn.config(state='disabled')
