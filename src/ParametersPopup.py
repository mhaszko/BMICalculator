import tkinter as tk
from tkinter import ttk
from ValidationSpinbox import ValidationSpinbox
from utilities import Person, FileData
from BMIWindow import BMIWindow


class ParametersPopup(tk.Toplevel):
    def __init__(self, master=None, login_session=None, data_instance=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

#       Configuration of popup
        self.height = 0
        self.weight = 0
        self.geometry('500x150')
        self.title('Insert your parameters !')
        self._person_instance = None
        self.login_session = login_session
        self._data_instance = data_instance
        self._params = (self.height, self.weight)
        self.params_list = ['' for i in range(5)]
        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)

#       Creation of object that will be used in ParametersPopup
        self.title = ttk.Label(self, text='Enter your height and weight:')
        self.height_lbl = ttk.Label(self, text='Height:')
        self.meters = ValidationSpinbox(self, upper_threshold=3, values=('0', '1', '2'))
        self.coma = ttk.Label(self, text=',')
        self.centimeters = ValidationSpinbox(self, upper_threshold=100, values=list(map(lambda x: str(x), range(0, 100))))
        self.meters_lbl = ttk.Label(self, text='m')
        self.weight_lbl = ttk.Label(self, text='Weight:')
        self.kg = ValidationSpinbox(self, upper_threshold=200, values=list(map(lambda x: str(x), range(0, 200))))
        self.coma_2 = ttk.Label(self, text=',')
        self.grams = ValidationSpinbox(self, upper_threshold=100, values=list(map(lambda x: str(x), range(0, 100))))
        self.kg_lbl = ttk.Label(self, text='kg')
        self.confirm_btn = ttk.Button(self, text='Confirm', state='disabled')

#       Binding button with confirm method
        self.confirm_btn.bind('<Button>', self.confirm)

#       Placing objects inside popup
        self.title.grid(row=0, column=0, columnspan=5)
        self.height_lbl.grid(row=1, column=0)
        self.meters.grid(row=1, column=1)
        self.coma.grid(row=1, column=2)
        self.centimeters.grid(row=1, column=3)
        self.meters_lbl.grid(row=1, column=4)
        self.weight_lbl.grid(row=2, column=0)
        self.kg.grid(row=2, column=1)
        self.coma_2.grid(row=2, column=2)
        self.grams.grid(row=2, column=3)
        self.kg_lbl.grid(row=2, column=4)
        self.confirm_btn.grid(row=3, column=0, columnspan=5)

#   Definition of methods
    def confirm(self, event):
        self.validate_input()
        if self._params != (0, 0):
            self._person_instance = Person(*self.params)
            self._data_instance.update_person_instance(self._person_instance)
            self._data_instance.save_to_file()
            self.display_info()

    def validate_input(self):
        self.params_list = [self.__getattribute__(instance).get() for instance in self.__dict__.keys() if
                            isinstance(self.__getattribute__(instance), ValidationSpinbox)]
        if all(self.params_list):
            self.height = float('.'.join(self.params_list[:2]))
            self.weight = float('.'.join(self.params_list[2:]))
            if self.height >= 0.5 and self.weight >= 20:
                self.confirm_btn.config(state='normal')
                self._params = (self.height, self.weight)
            else:
                self.confirm_btn.config(state='disabled')
        else:
            self.confirm_btn.config(state='disabled')

    def display_info(self):
        self.info_popup = tk.Toplevel(self)
        self.info_popup.info_lbl = ttk.Label(self.info_popup, text='Your update was saved !', justify='center')
        self.info_popup.confirm_btn = ttk.Button(self.info_popup, text='Ok !', command=self.widget_closing)
        self.info_popup.info_lbl.pack()
        self.info_popup.confirm_btn.pack()

    def widget_closing(self):
        self.destroy()

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._params = value
