import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utilities import *

#Main windows creation
window = tk.Tk()
window.geometry('1000x300')
window.resizable(False, False)
window.title('BMI Calculator')


#Frames definition
menu_frame = tk.Frame(window)
main_frame = tk.Frame(window)

login_session=Login()

class HintCombobox(ttk.Combobox):
    def __init__(self, master=None, placeholder='', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_color=self['foreground']

        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self.config(foreground=self.placeholder_color, font=('Corbel', 12, 'italic'))

    def focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, 'end')
            self.config(foreground=self.default_color, font=('Corbel', 12, 'bold'))

    def focus_out(self, event):
        if not self.get():
            self.put_placeholder()

    def reconfig(self, event):
        self.config(foreground=self.default_color, font=('Corbel', 12, 'bold'))


class ValidationSpinbox(ttk.Spinbox):
    def __init__(self, master=None, threshold=100, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.treshold = threshold

        self.bind('<KeyRelease>', self.compare_value)

    def compare_value(self, event):
        if int(self.get()) >= self.treshold:
            self.delete(0, 'end')
            self.insert(0, str(self.treshold - 1))

FileData.get_files()
nicks = [file_name[:-4] for file_name in FileData.filelist]

menu_frame.place(x=0, y=0, relwidth=.3, relheight=1)
main_frame.place(relx=.3, y=0, relwidth=.7, relheight=1)


def combobox_selected(event):
    login_btn.config(state='normal')
    login_cmb.config(foreground='black', font=('Corbel', 12, 'bold'))

def change_btn_state(event):
    if login_cmb.get():
        login_btn.config(state='normal')
    else:
        login_btn.config(state='disabled')

def open_popup():
    error_pop = tk.Toplevel(window)
    error_pop.title("Wrong input")
    tk.Label(error_pop, text="Nick can't contain special signs !", font=('Corbel', 12, 'bold')).grid(row=0)
    tk.Button(error_pop, text='Ok !', font=('Corbel', 12, 'bold'), command=error_pop.destroy).grid(row=1)

def login():
    if login_cmb.get().isalnum():
        if not login_session.login_status:
            login_session.login(login_cmb.get())
            login_btn.config(state='disabled')
            welcome_lb.config(text=f'Welcome {login_session.nick} !\nWhat do You want to do ?')
    else:
        open_popup()

def parameters_popup():
    params_popup = tk.Toplevel(window)
    params_popup.geometry('500x150')
    params_popup.rowconfigure((0, 1, 2, 3), weight=1)
    params_popup.columnconfigure((0, 1, 2, 3, 4), weight=1)
    ttk.Label(params_popup, text='Enter your height and weight:').grid(row=0, column=0, columnspan=5)
    ttk.Label(params_popup, text='Height:').grid(row=1, column=0)
    ValidationSpinbox(params_popup, threshold=3, values=('0', '1', '2')).grid(row=1, column=1)
    ttk.Label(params_popup, text=',').grid(row=1, column=2)
    ValidationSpinbox(params_popup, threshold=100, values=list(map(lambda x: str(x), range(0, 100)))).grid(row=1, column=3)
    ttk.Label(params_popup, text='m').grid(row=1, column=4)
    ttk.Label(params_popup, text='Weight:').grid(row=2, column=0)
    ValidationSpinbox(params_popup, threshold=200, values=list(map(lambda x: str(x), range(0, 200)))).grid(row=2, column=1)
    ttk.Label(params_popup, text=',').grid(row=2, column=2)
    ValidationSpinbox(params_popup, threshold=100, values=list(map(lambda x: str(x), range(0, 100)))).grid(row=2, column=3)
    ttk.Label(params_popup, text='kg').grid(row=2, column=4)
    ttk.Button(params_popup, text='Confirm').grid(row=3, column=0, columnspan=5)

#Preparation of image
image = Image.open('shutterstock_1341869564.jpg').resize((300, 136))
image_tk = ImageTk.PhotoImage(image)

#Menu widget creation
logo_lb = ttk.Label(menu_frame, image=image_tk)
login_btn = ttk.Button(menu_frame, text='Login', state='disabled', command=login)
login_cmb = HintCombobox(menu_frame, values=nicks, justify='center', placeholder='Please insert your nick', font=('Corbel', 12, 'italic'))

#Main widgets creation
welcome_lb = ttk.Label(main_frame, text='Welcome !', font=('Corbel', 12, 'bold'), justify='center')
parameters_btn = ttk.Button(main_frame, text='Add measurement', command=parameters_popup)
bmi_btn = ttk.Button(main_frame, text='Check your progress !')
calories_btn = ttk.Button(main_frame, text='Check your demands !')
update_btn = ttk.Button(main_frame, text='Update your reccords !')
logout_btn = ttk.Button(main_frame, text='Logout !')

#Events:
login_cmb.bind('<<ComboboxSelected>>', combobox_selected)
login_cmb.bind('<KeyRelease>', change_btn_state)

#Menu frame configuration:
menu_frame.columnconfigure((0), weight=1)
menu_frame.rowconfigure((0, 1, 2, 3), weight=1)

#Main frame configuration:
main_frame.columnconfigure((0, 1), weight=1)
main_frame.rowconfigure((0, 1, 2), weight=1)

#Widgets addition to menu frame
logo_lb.grid(row=0)
login_cmb.grid(row=1)
login_btn.grid(row=2)

#Widgets addition to main frame
welcome_lb.grid(row=0, column=0, columnspan=2)
parameters_btn.grid(row=1, column=0, sticky='nsew')
bmi_btn.grid(row=1, column=1, sticky='nsew')
calories_btn.grid(row=1, column=2, sticky='nsew')
update_btn.grid(row=2, column=0, columnspan=2, sticky='nsew')
logout_btn.grid(row=2, column=2, sticky='nsew')

#run

window.mainloop()