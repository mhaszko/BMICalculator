import os

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from utilities import *

class ScreenUtility(Screen):
    def __init__(self, **kwargs):
        super(ScreenUtility, self).__init__(**kwargs)

        #Ustawienie parametrów aplikacji:
        self.background_color = (1, 1, 1, 1)
        #self.size_hint = (0.8, 0.6)

        self.shutdown_button = Button(
            text='Exit',
            size_hint=(None, None),
            size=(100, 40),
            pos=(Window.width - 120, Window.height - 60)
        )
        self.shutdown_button.bind(on_press=self.shutdown_app)
        self.add_widget(self.shutdown_button)

    @staticmethod
    def shutdown_app():
        Window.close()


class LoginScreen(ScreenUtility):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.nicks = None

        # Dodanie etykiety "Login" na środku ekranu
        self.login_label = Label(
            text='Login',
            font_size=40,
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        self.add_widget(self.login_label)

        # Tworzymy pole do wprowadzania tekstu
        self.nick_input = TextInput(
            hint_text='Enter your nick',
            multiline=False,
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.4, 'center_y': 0.5}
        )
        self.add_widget(self.nick_input)

        if self.nicks is None:
            FileData.get_files()
            self.nicks = [file_name[:-4] for file_name in FileData.filelist]

        self.spinner = Spinner(
            text='or choose saved one.',
            values=self.nicks,
            size_hint=(None, None),
            size=(250, 50),
            pos_hint = {
                    'center_x': self.nick_input.pos_hint['center_x'] +
                                (self.nick_input.size[0] + self.size[0] / 2) / 1000,
                    'center_y': self.nick_input.pos_hint['center_y']}
        )
        self.spinner.bind(text=self.on_spinner_text)
        self.add_widget(self.spinner)

        self.confirmation_button = Button(
            text='Confirm',
            size_hint=(None, None),
            size=(100, 40),
            pos_hint={'center_x': 0.5, 'center_y': self.nick_input.pos_hint['center_y'] - self.size[1] / 1000},
            on_press=self.check_input
        )
        self.add_widget(self.confirmation_button)

        self.popup = Popup(
            title='You have to insert your login ! ',
            size_hint=(None, None),
            size=(250, 100)
        )
        self.popup.content = Button(
            text='OK !',
            #size=(self.popup.size[0], 10),
            on_press=self.popup.dismiss
        )

    def on_spinner_text(self, spinner, text):
        # Jeśli użytkownik wybierze wartość z listy, aktualizujemy wartość w polu do wprowadzania tekstu
        if text in spinner.values:
            self.nick_input.text = text

    def switch_screen(self, instance):
        self.manager.current = 'second'

    def check_input(self, instance):
        if self.nick_input.text:
            self.switch_screen(self)
        else:
            self.popup.open()


class SecondScreen(ScreenUtility):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        layout = Button(text='Powrót do pierwszego ekranu', on_press=self.switch_screen)
        self.add_widget(layout)

    def switch_screen(self, instance):
        self.manager.current = 'main'

class MyApp(App):
    def build(self):
        # Tworzymy ekran managera
        sm = ScreenManager()

        # Dodajemy ekrany do managera
        sm.add_widget(LoginScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))

        return sm

if __name__ == '__main__':
    MyApp().run()
