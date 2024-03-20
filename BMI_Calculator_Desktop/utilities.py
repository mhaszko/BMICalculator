import os
import time


class Login:
    """Class Login, made to create login instance \"session\" and manage it
    for user specified by nick parameter """
    _logged_user = None

    def __new__(cls, *args, **kwargs):
        if cls._logged_user is None:
            cls._logged_user = object.__new__(cls)
        return cls._logged_user

    def __init__(self, nick=''):
        self.nick = nick
        self.login_status = False

    @property
    def nick(self):
        return self._nick

    @nick.setter
    def nick(self, value):
        if value.isalnum():
            self._nick = value

    def login(self, nick):
        self.nick = nick
        self.login_status = True

    def logout(self):
        self.nick = ''
        self.login_status = False






class Person:
    """
    Class Person used to create person object describing parameters of persons using the BMI calculator.
    """
    def __init__(self, height, weight, ):
        self.height = height
        self.weight = weight
        self._bmi = None

    @property
    def bmi(self):
        if self._bmi is None:
            self._bmi = self.weight / self.height ** 2
        return self._bmi

    def bmi_classification(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return  'Normal'
        elif bmi < 30:
            return 'Overweight'
        elif bmi < 35:
            return 'Obese'
        else:
            return 'Extremely Obese'

    @property
    def params(self):
        return [time.ctime()] + [f'{key}: {val}' for key, val in self.__dict__.items()
                                 if not key.startswith('_')] + [f'bmi: {self._bmi:.2f}']

class Propositions:
    activity_rate = {}
    def __init__(self, person_instance):
        self.person_instance = person_instance
        self._zero_calorical = None

    @property
    def zero_calorical(self):
        if self._zero_calorical is None:
            pass


class FileData:
    filelist = []
    def __init__(self, login_instance):
        self._filename = None
        self._dirlist = None
        self.login_instance = login_instance

    @property
    def filename(self):
        if self._filename is None:
            self._filename = f'{self.login_instance.nick}.txt'
        return self._filename
    @classmethod
    def get_files(cls):
        cls.filelist = os.listdir('./users_data/')

    def isuserfile(self):
        return self._filename in FileData.filelist

    def save_to_file(self, person_instance):
        parameter_string = '|'.join(person_instance.params)
        print(parameter_string)