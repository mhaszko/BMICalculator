import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utilities import FileData
from HintCombobox import HintCombobox


class MenuFrame(tk.Frame):
    def __init__(self, master=None, login_session=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
#   Creating objects of menu frame
        self.login_session = login_session
        self.image = Image.open('shutterstock_1341869564.jpg').resize((300, 136))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.logo_lb = ttk.Label(
            self,
            image=self.image_tk
        )
        self.login_btn = ttk.Button(
            self,
            text='Login',
            state='disabled',
            command=login
        )
        FileData.get_files()
        self.nicks = [file_name[:-4] for file_name in FileData.filelist]
        self.login_cmb = HintCombobox(
            self,
            values=self.nicks,
            justify='center',
            placeholder='Please insert your nick',
            font=('Corbel', 12, 'italic')
        )

#   Menu frame grid configuration:
        self.columnconfigure((0), weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

#   Placing prepared widgets to menu frame
        self.logo_lb.grid(row=0)
        self.login_cmb.grid(row=1)
        self.login_btn.grid(row=2)

#   Binding methods to specific events
        self.login_cmb.bind('<<ComboboxSelected>>', self.combobox_selected)
        self.login_cmb.bind('<KeyRelease>', self.change_btn_state)

#   Defining needed methods
    def combobox_selected(self, event):
        self.login_btn.config(state='normal')
        self.login_cmb.config(foreground='black', font=('Corbel', 12, 'bold'))

    def change_btn_state(self, event):
        if self.login_cmb.get():
            self.login_btn.config(state='normal')
        else:
            self.login_btn.config(state='disabled')


    def login(self):
        if self.login_cmb.get().isalnum():
            if not self.login_session.login_status:
                self.login_session.login(self.login_cmb.get())
                self.login_btn.config(state='disabled')
                self.login_cmb.config(state='disabled')
                self.welcome_lb.config(text=f'Welcome {self.login_session.nick} !\nWhat do You want to do ?')
        else:
            self.open_popup()

    def open_popup(self):
        error_pop = tk.Toplevel(window)
        error_pop.title("Wrong input")
        tk.Label(error_pop, text="Nick can't contain special signs !", font=('Corbel', 12, 'bold')).grid(row=0)
        tk.Button(error_pop, text='Ok !', font=('Corbel', 12, 'bold'), command=error_pop.destroy).grid(row=1)