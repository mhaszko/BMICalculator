from tkinter import ttk


class LoggedButton(ttk.Button):
    """Class LoggedButton inherits from ttk.Button class.
    It requires additional login_instance parameter during construction of it,
     and its state depends on state of login_instance"""
    def __init__(self, master=None, login_instance=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.login_instance = login_instance

        self.bind('<Button>', self.focus_in)

        self.verify_login_state()

    def focus_in(self, event):
        self.verify_login_state()

    def verify_login_state(self):
        if self.login_instance.login_status:
            self.config(state='normal')
        else:
            self.config(state='disabled')