from tkinter import ttk


class LoggedButton(ttk.Button):
    """
    Class LoggedButton inherits from ttk.Button class. Button state depends on login state.
    :param login_instance: takes login_instance created after user login to app
    """
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