from tkinter import ttk

class ValidationSpinbox(ttk.Spinbox):
    """Class ValidationSpinbox inherits from ttk.Spinbox class.
    It adds input validation to standard Spinbox functionalities"""
    def __init__(self, master=None, lower_threshold=None, upper_threshold=100, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

        self.bind('<FocusOut>', self.compare_value)

    def compare_value(self, event):
        if self.get().isnumeric():
            if self.lower_threshold:
                try:
                    if int(self.get()) < self.lower_threshold:
                        self.delete(0, 'end')
                        self.insert(0, str(self.lower_threshold))
                except ValueError:
                    self.insert(0, '0')
            try:
                if int(self.get()) >= self.upper_threshold:
                    self.delete(0, 'end')
                    self.insert(0, str(self.upper_threshold - 1))
            except ValueError:
                self.insert(0, '0')
        else:
            self.delete(0, 'end')