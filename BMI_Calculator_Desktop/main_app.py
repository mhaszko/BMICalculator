import tkinter as tk

from ParametersPopup import ParametersPopup
from MenuFrame import MenuFrame
from MainWindow import MainWindow


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
            login_cmb.config(state='disabled')
            welcome_lb.config(text=f'Welcome {login_session.nick} !\nWhat do You want to do ?')
    else:
        open_popup()


def logout():
    login_session.logout()
    login_btn.config(state='normal')
    login_cmb.config(state='normal')
    welcome_lb.config(text=f'Cya !\nThank You for using this app !')


def parameters_popup():
    params_popup = ParametersPopup(window)


#run
if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
