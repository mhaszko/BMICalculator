import tkinter as tk
from tkinter import ttk

from ParametersPopup import ParametersPopup
from LoggedButton import LoggedButton

class MainFrame(tk.Frame):
    def __init__(self, login_session=None, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.login_session = login_session
        self.parameters_popup = ParametersPopup()
        self.welcome_lb = ttk.Label(
            self,
            text='Welcome !',
            font=('Corbel', 12, 'bold'),
            justify='center'
        )
        self.parameters_btn = LoggedButton(
            self,
            login_instance=self.login_session,
            text='Add measurement',
            command=self.parameters_popup
        )
        self.bmi_btn = LoggedButton(
            self,
            login_instance=self.login_session,
            text='Check your progress !'
        )
        self.calories_btn = LoggedButton(
            self,
            login_instance=self.login_session,
            text='Check your needs !'
        )
        self.update_btn = LoggedButton(
            self,
            login_instance=self.login_session,
            text='Update your records !'
        )
        self.logout_btn = LoggedButton(
            self,
            login_instance=self.login_session,
            text='Logout !',
            command=logout
        )
#   Main frame grid configuration:
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

#   Placing main frame widgets in the grid
        self.welcome_lb.grid(row=0, column=0, columnspan=2)
        self.parameters_btn.grid(row=1, column=0, sticky='nsew')
        self.bmi_btn.grid(row=1, column=1, sticky='nsew')
        self.calories_btn.grid(row=1, column=2, sticky='nsew')
        self.update_btn.grid(row=2, column=0, columnspan=2, sticky='nsew')
        self.logout_btn.grid(row=2, column=2, sticky='nsew')

#   Defining necessary methods
    def logout(self):
        self.login_session.logout()
        login_btn.config(state='normal')
        login_cmb.config(state='normal')
        self.welcome_lb.config(text=f'Cya !\nThank You for using this app !')
