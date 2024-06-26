import tkinter as tk

from utilities import Login
from MenuFrame import MenuFrame
from MainFrame import MainFrame


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('1000x300')
        self.resizable(False, False)
        self.title('BMI Calculator')
        self.login_session = Login()
        self.menu_frame = MenuFrame(self, self.login_session)
        self.main_frame = MainFrame(self, self.login_session)
        self.menu_frame.place(x=0, y=0, relwidth=.3, relheight=1)
        self.main_frame.place(relx=.3, y=0, relwidth=.7, relheight=1)