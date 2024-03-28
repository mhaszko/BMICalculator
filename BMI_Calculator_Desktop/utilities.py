import os
import time
from datetime import date, datetime


class Login:
    """Class Login, made to create login instance \"session\" and manage it
    for user specified by nick parameter """
    _logged_user = None

    def __new__(cls, *args, **kwargs):
        if cls._logged_user is None:
            cls._logged_user = object.__new__(cls)
        return cls._logged_user

    def __init__(self, nick=''):
        self._nick = nick
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
    def __init__(self, height, weight):
        self.height = height
        self.weight = weight
        self._bmi = None

    @property
    def bmi(self):
        if self._bmi is None:
            self._bmi = self.weight / self.height ** 2
        return self._bmi

    def bmi_classification(self):
        bmi = self.bmi
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        elif bmi < 35:
            return 'Obese'
        else:
            return 'Extremely Obese'


class Propositions:
    """
    Class Propoistion i dunno yet whats the logic behind it
    """
    activity_rate = {}
    def __init__(self, person_instance):
        self.person_instance = person_instance
        self._zero_calorical = None

    @property
    def zero_calorical(self):
        if self._zero_calorical is None:
            pass


class FileData:
    """
    Class FileData is being used to manage the saving/reading data stored in files.
    nick :param - used to determine the file name, should be the nick out of login instance
    person_instance :param - used to append
    """
    filelist = []

    def __init__(self, nick, person_instance=None):
        self._filename = None
        self._dirlist = None
        self._data_to_save = None
        self._params = None
        self.nick = nick
        self.person_instance = person_instance

    @property
    def filename(self):
        if self._filename is None:
            self._filename = f'{self.nick}.txt'
        return self._filename

    @classmethod
    def get_files(cls):
        cls.filelist = os.listdir('./users_data/')

    # @property
    # def person_instance(self):
    #     return self._person_instance

    # @person_instance.setter
    # def person_instance(self, value):
    #     self._person_instance = value

    def update_person_instance(self, value):
        self.person_instance = value

    @property
    def params(self):
        if self._params is None:
            self._params = ([date.today().strftime("%Y-%m-%d")] +
                    [f'{key}: {val}' for key, val in self.person_instance.__dict__.items()if not key.startswith('_')] +
                    [f'bmi: {self.person_instance.bmi:.2f}'])
        return self._params

    def isuserfile(self):
        return self.filename in FileData.filelist

    def get_records(self):
        try:
            with open(f'./users_data/{self.filename}', 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            with open(f'./users_data/{self.filename}', 'w') as file:
                file.write('')
                lines = []
        return lines

    def get_dates_from_file(self):
        lines = self.get_records()
        return list(map(lambda line: line.split('|')[0], lines))

    def get_bmi_from_file(self):
        lines = self.get_records()
        return [line.split('|')[-1].split(' ')[-1].strip() for line in lines]

    def get_height_from_file(self):
        lines = self.get_records()
        return [line.split('|')[1].split(' ')[-1] for line in lines]

    def get_weight_from_file(self):
        lines = self.get_records()
        return [line.split('|')[2].split(' ')[-1] for line in lines]

    def last_record_person_instance(self):
        return Person(float(self.get_height_from_file()[-1]), float(self.get_weight_from_file()[-1]))

    def get_last_date(self):
        lines = self.get_records()
        last_date = list(map(lambda x: int(x), lines[-1].split('|')[0].split('-')))
        return datetime(*last_date).date()

    def param_str(self):
        return '|'.join(self.params) + '\n'

    def save_to_file(self):
        if self.get_records():
            if self.get_last_date() == date.today():
                lines = self.get_records()
                with open(f'./users_data/{self.filename}', 'w') as file:
                    for line in lines[:-1]:
                        file.write(line)
        with open(f'./users_data/{self.filename}', 'a') as file:
            file.write(self.param_str())
