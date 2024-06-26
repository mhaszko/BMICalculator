import tkinter as tk
from tkinter import ttk

from ParametersPopup import ParametersPopup
from LoggedButton import LoggedButton
from BMIWindow import BMIWindow
from ARQuestion import ARQuestion
from utilities import FileData


class MainFrame(tk.Frame):
    """
    Class MainFrame inherits from tk.Frame and adds specific widgets for specific use inside BMICalculator.
    :param login_session: takes login_session created after login. This param is used to
    control the state of logged buttons inside this frame
    """
    def __init__(self, master=None, login_session=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.login_session = login_session
        self._data_instance = None
        self.parameters_popup = None
        self.bmi_window = None
        #Creating specific widgets
        self.welcome_lb = ttk.Label(
            self,
            text='Welcome !',
            font=('Corbel', 12, 'bold'),
            justify='center'
        )
        self.parameters_btn = LoggedButton(
            self,
            login_instance=self.login_session,
            text='Add measurement !',
            command=self.open_popup
        )
        self.bmi_btn = LoggedButton(
            self,
            login_instance=self.login_session,
            text='Check your progress !',
            command=self.open_bmi_information
        )
        self.calories_btn = LoggedButton(
            self,
            login_instance=self.login_session,
            text='Check your needs !',
            command=self.open_needs_information
        )
        self.logout_btn = LoggedButton(
            self,
            login_instance=self.login_session,
            text='Logout !',
            command=self.logout
        )
#   Main frame grid configuration:
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

#   Placing main frame widgets in the grid
        self.welcome_lb.grid(row=0, column=0, columnspan=2)
        self.parameters_btn.grid(row=1, column=0, sticky='nsew')
        self.bmi_btn.grid(row=1, column=1, sticky='nsew')
        self.calories_btn.grid(row=2, column=0, sticky='nsew')
        self.logout_btn.grid(row=2, column=1, sticky='nsew')

    #Defining necessary methods
    def open_popup(self):
        self.parameters_popup = ParametersPopup(
            master=self.master,
            login_session=self.login_session,
            data_instance=self.data_instance
        )

    def open_bmi_information(self):
        if self.data_instance.get_records():
            self.bmi_window = BMIWindow(
                master=self,
                data_instance=self.data_instance,
                nick=self.login_session.nick
            )
        else:
            self.info_window()

    def open_needs_information(self):
        if self.data_instance.get_records():
            self.ar_question = ARQuestion(self, self.data_instance, self.login_session.nick)
        else:
            self.info_window()

    def logout(self):
        self.login_session.logout()
        FileData.get_files()
        self.master.menu_frame.login_btn.config(state='normal')
        self.master.menu_frame.login_cmb.config(state='normal')
        self.master.menu_frame.login_cmb.config(values=[file_name[:-4] for file_name in FileData.filelist])
        self.data_instance = None
        self.welcome_lb.config(text=f'Cya !\nThank You for using this app !')


    def info_window(self):
        self._info_window = tk.Toplevel(self)
        self._info_window.info_lbl = ttk.Label(
            self._info_window,
            text='You have no records to display yet !',
            justify='center'
        )
        self._info_window.confirm_btn = ttk.Button(
            self._info_window,
            text='Ok !',
            command=self.widget_closing
        )
        self._info_window.info_lbl.pack()
        self._info_window.confirm_btn.pack()

    def widget_closing(self):
        self._info_window.destroy()

    @property
    def data_instance(self):
        return self._data_instance

    @data_instance.setter
    def data_instance(self, value: FileData):
        self._data_instance = value