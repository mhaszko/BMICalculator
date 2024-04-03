import tkinter as tk
from tkinter import ttk
from utilities import FileData, Person
from datetime import datetime, date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class BMIWindow(tk.Toplevel):
    """
    Class BMIWindow inherits from tk.TopLevel and adds specific widgets for specific use inside BMICalculator.
    :param data_instance: takes data_instance created for specific user after login
    :param nick: takes nick variable out of login_instance made for specific user after login
    """
    def __init__(self, master=None, data_instance=None, nick=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        #self.geometry('600x400')
        self.resizable(False, False)
        self.title('BMI')
        self.nick = nick
        self.data_instance = data_instance
        self.person_instance = self.data_instance.last_record_person_instance()
        ##Creating widgets that will be used inside this window
        self.welcome_label = self.create_welcome_label()
        self.bmi_label = ttk.Label(
            self,
            text=f'Your BMI equals:\n{self.person_instance.bmi:.2f}\n'
                f'You are {self.person_instance.bmi_classification()}',
            font=('Corbel', 16, 'bold'),
            justify='center',
            foreground=self.choose_color(),
            relief="solid"
            )
        self.create_plot()
        self.change_lbl = ttk.Label(
            self,
            text=self.get_text(),
            font=('Corbel', 16, 'bold'),
            justify='center'
        )
        self.close_btn = ttk.Button(self, text='Close', command=self.destroy)

        # Putting the widgets into the window
        self.welcome_label.grid(row=0, column=0, columnspan=2) #sticky='nsew')
        self.bmi_label.grid(row=1, column=1, sticky='nsew')
        self.change_lbl.grid(row=2, column=0, sticky='nsew')
        self.close_btn.grid(row=2, column=1, sticky='nsew')

    #Defining necessary methods
    def count_days(self):
        """
        :return: difference between current date and date of last app usage obtained from data_instance
        """
        return date.today() - self.data_instance.get_last_date()

    def create_welcome_label(self):
        """
        :return: Specific welcome label with calculated days from last usage of app if the app was used before, or
        only welcome label without calculated days if its first use of this app
        """
        if self.data_instance.isuserfile():
            return ttk.Label(
                self,
                text=f'Hello {self.nick} !\n It was {str(self.count_days()).split(',')[0]} since your last visit !',
                font=('Corbel', 16, 'bold'),
                justify='center',
                relief="solid"
            )
        else:
            return ttk.Label(
                self,
                text=f'Hello {self.nick} !\n It\'s your first use of this application !',
                justify='center',
                font=('Corbel', 16, 'bold'),
                relief="solid"
            )

    def choose_color(self):
        """
        :return: Color of bmi classification label, according to bmi value.
        """
        if self.person_instance.bmi_classification() == 'Underweight':
            return 'yellow'
        elif self.person_instance.bmi_classification() == 'Normal':
            return 'green'
        elif self.person_instance.bmi_classification() == 'Overweight':
            return 'orange'
        else:
            return 'red'

    def create_plot(self):
        """
        Creates graph that displays user's progress if user updated his params for more than once,
        else creates the excuse label.
        """
        if len(self.data_instance.get_records()) > 1:
            fig, ax = plt.subplots()
            ax.plot(
                self.data_instance.get_dates_from_file(),
                self.data_instance.get_bmi_from_file(),
                color='r',
                label='BMI'
            )
            ax.plot(
                self.data_instance.get_dates_from_file(),
                self.data_instance.get_weight_from_file(),
                color='g',
                label='Weight'
            )
            ax.legend()
            ax.set_title('Weight changes !', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date', fontsize=12)
            self.bmi_plot = FigureCanvasTkAgg(fig, master=self)
            self.bmi_plot.draw()
            self.bmi_plot.get_tk_widget().grid(row=1, column=0)
        else:
            self.excuse_label = ttk.Label(
                self,
                text=f'If you had used this app before,\n'
                     f' there would have been a graph showing your progress here!',
                font=('Corbel', 16, 'bold'),
                justify='center',
                relief="solid"
            )
            self.excuse_label.grid(row=1, column=0, sticky='nsew')

    def get_text(self):
        """
        :return: text to change_lbl, according to change of user's weight
        """
        if len(self.data_instance.get_records()) > 1:
            last_weight = float(self.data_instance.get_weight_from_file()[-1])
            prelast_weight = float(self.data_instance.get_weight_from_file()[-2])
            if last_weight > prelast_weight:
                return f'You\'ve gained {last_weight - prelast_weight:.2f} !'
            elif last_weight == prelast_weight:
                return 'Your weight stays the same !'
            else:
                return f'You\'ve lost {prelast_weight - last_weight:.2f} !'
