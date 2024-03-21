from tkinter import ttk


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