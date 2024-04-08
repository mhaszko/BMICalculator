import tkinter as tk
from tkinter import ttk


class MetabolismWindow(tk.Toplevel):
    """
    Class MetabolismWindow inherits from tk.TopLevel and adds specific widgets for specific use inside BMICalculator.
    :param proposition_instance: takes proposition_instance created after confirming input inside ARQuestion
    :param nick: takes nick variable out of login_instance made for specific user after login
    """
    def __init__(self, master, proposition_instance, nick, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.proposition_instance = proposition_instance
        self.nick = nick
        self.calories = self.proposition_instance.total_metabolism
        self.protein_percent = None
        self.fat_percent = 30
        self.carbo_percent = None
        self.labels = ['Proteins', 'Fats', 'Carbohydrates']
        # Creating widgets that will be inside this info window
        self.main_lbl = ttk.Label(
            self,
            text=f'{self.nick.capitalize()} your total metabolism '
                 f'equals {self.proposition_instance.total_metabolism:.2f} kcal !',
            font=('Corbel', 16, 'bold'),
            justify='center'
        )
        self.info_lbl = ttk.Label(
            self,
            text=self.get_text(),
            font=('Corbel', 14, 'bold'),
            justify='center'
        )
        self.nutrients_lbl = ttk.Label(
            self,
            text=f'At {self.calories:.2f} calories, the macronutrients are:\n'
                 f'Proteins: {self.nutrients_grams(self.calories)[0]:.2f} g\n'
                 f'Fats: {self.nutrients_grams(self.calories)[1]:.2f} g\n'
                 f'Carbohydrates: {self.nutrients_grams(self.calories)[2]:.2f} g',
            font=('Corbel', 14),
            justify='left'
        )
        self.scale = ttk.Scale(
            self,
            from_=0.1,
            to=2,
            length=100,
            orient=tk.VERTICAL,
            command=self.update_calories
        )
        self.scale.set(1)
        self.close_btn = ttk.Button(self, text='Close', command=self.close)

        # Putting specific widgets inside the window

        self.main_lbl.grid(row=0, column=0, columnspan=2)
        self.info_lbl.grid(row=1, column=0, columnspan=2)
        self.nutrients_lbl.grid(row=2, column=0)
        self.scale.grid(row=2, column=1)
        self.close_btn.grid(row=3, column=1)

    def get_text(self):
        if self.proposition_instance.person_instance.bmi < 18.5:
            return 'According to your BMI,\nYou should gain weight'
        elif self.proposition_instance.person_instance.bmi < 25:
            return 'According to your BMI,\nYou should maintain weight'
        else:
            return 'According to your BMI,\nYou should lose weight'

    def calculate_proportions(self, variable):
        self.protein_percent = self.proposition_instance.person_instance.weight * 800 / variable
        self.carbo_percent = ((variable -
                              variable * (self.protein_percent / 100) -
                              variable * (self.fat_percent / 100)) / variable) * 100
        return [
            self.protein_percent,
            self.fat_percent,
            self.carbo_percent
        ]

    def nutrients_grams(self, variable):
        solution = []
        for index, percent in enumerate(self.calculate_proportions(variable)):
            gram = 4
            if index == 1:
                gram = 9
            solution.append((percent / 100) * variable / gram)
        return solution

    def update_calories(self, event):
        value = self.scale.get()
        _calories = self.calories
        _calories *= value
        self.nutrients_lbl.config(text=f'At {_calories:.2f} calories, the macronutrients are:\n'
            f'Proteins: {self.nutrients_grams(_calories)[0]:.2f} g\n'
            f'Fats: {self.nutrients_grams(_calories)[1]:.2f} g\n'
            f'Carbohydrates: {self.nutrients_grams(_calories)[2]:.2f} g')

    def close(self):
        self.master.destroy()
        self.destroy()
