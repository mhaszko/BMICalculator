from tkinter import ttk

class ValidationSpinbox(ttk.Spinbox):
    """Class ValidationSpinbox inherits from ttk.Spinbox class.
    It adds input validation to standard Spinbox functionalities"""
    def __init__(self, master=None, threshold=100, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.threshold = threshold

        self.bind('<FocusOut>', self.compare_value)

    def compare_value(self, event):
        if self.get().isnumeric():
            try:
                if int(self.get()) >= self.threshold:
                    self.delete(0, 'end')
                    self.insert(0, str(self.threshold - 1))
            except ValueError:
                self.insert(0, '0')
        else:
            self.delete(0, 'end')