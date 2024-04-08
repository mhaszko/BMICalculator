import os
import time
from datetime import date, datetime


class Login:
    """
    Class Login, made to create login instance \"session\" and manage it
    for user specified by nick parameter
    :param nick: takes nick that will be used to distinguish sepcific user
    """
    _logged_user = None

    # def __new__(cls, *args, **kwargs):
    #     if cls._logged_user is None:
    #         cls._logged_user = object.__new__(cls)
    #     return cls._logged_user

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

    def login(self, nick: str):
        """
        :param nick: takes nick to change session state
        :return: None
        """
        self.nick = nick
        self.login_status = True

    def logout(self):
        self.nick = ''
        self.login_status = False


class Person:
    """
    Class Person used to create person object describing parameters of persons using the BMI calculator.
    :param height: takes user's height to specify his bmi etc.
    :param weight: takes user's weight to specify his bmi etc.
    """
    def __init__(self, height, weight):
        self.height = height
        self.weight = weight
        self._bmi = None

    @property
    def bmi(self) -> float:
        """
        Basing on person_instance params sets bmi value
        :return: person instance bmi value
        """
        if self._bmi is None:
            self._bmi = self.weight / self.height ** 2
        return self._bmi

    def bmi_classification(self) -> str:
        """
        :return: Classification of the user basing on his bmi
        """
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

    def convert_height(self) -> int:
        """
        Function made to convert person's height given in x.yy m format to yyy cm format
        :return: person's height in cm
        """
        return self.height * 100


class Propositions:
    """
    Class Propositions used to create propositions object describing calorical and nutrient needs of
     persons using the BMI calculator.
    :param person_instance: takes user's person_instance to specify user's params and basing on it calculate suitable
    nutrients values
    :param age: takes user's age to calculate his total metabolism
    :param gender: takes user's gender to calculate his total metabolism and his nutrient needs
    :param activity_rate: takes user's activity_rate to calculate his total metabolism
    """
    activity_factors = {
        '1': 1.4,
        '2': 1.55,
        '3': 1.85,
        '4': 2.1,
        '5': 2.3
    }
    def __init__(self, person_instance, age, gender, activity_rate):
        self.person_instance = person_instance
        self.age = age
        self.gender = gender
        self.activity_rate = activity_rate.split(' ')[0]
        self._total_metabolism = None

    @property
    def total_metabolism(self) -> float:
        """
        Basing on proposition_instance calculates the user's total_metabolism
        :return: user's total metabolism
        """
        if self._total_metabolism is None:
            if self.gender == 'female':
                self._total_metabolism = Propositions.activity_factors[self.activity_rate] * (
                        (10 * self.person_instance.weight) + (6.25 * self.person_instance.convert_height()) -
                        (5 * self.age) - 161)
            else:
                self._total_metabolism = Propositions.activity_factors[self.activity_rate] * (
                        (10 * self.person_instance.weight) + (6.25 * self.person_instance.convert_height()) -
                        (5 * self.age) + 5)
        return self._total_metabolism


class FileData:
    """
    Class FileData is being used to manage the saving/reading data stored in files.
    :param nick: takes user's nick, used to determine the file name,
    :param person_instance: takes person_instance, so new records can be added to user's file
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
    def filename(self) -> str:
        """
        Sets filename basing on object's nick
        :return: filename
        """
        if self._filename is None:
            self._filename = f'{self.nick}.txt'
        return self._filename

    @classmethod
    def get_files(cls):
        """
        Class method used to update class's filelist attribute
        :return: None
        """
        cls.filelist = os.listdir('./users_data/')

    def update_person_instance(self, value: Person):
        """
        Method made to update object's person_instance
        :param value: takes person_instance to update the person_instance object's attribute
        :return: None
        """
        self.person_instance = value

    @property
    def params(self) -> list[str]:
        """
        Method made to create list of params that will be saved to file
        :return: list[str] that contatins user's params
        """
        if self._params is None:
            self._params = ([date.today().strftime("%Y-%m-%d")] +
                    [f'{key}: {val}' for key, val in self.person_instance.__dict__.items()if not key.startswith('_')] +
                    [f'bmi: {self.person_instance.bmi:.2f}'])
        return self._params

    def isuserfile(self) -> bool:
        """
        Method to check if specific user's file is already inside users_data
        :return: True if user's file is already made
        """
        return self.filename in FileData.filelist

    def get_records(self) -> list[str]:
        """
        Method to read user's record from file if file exists or creates the file if it doesn't exist
        :return: List[str] where one list index is one line read from file
        """
        try:
            with open(f'./users_data/{self.filename}', 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            with open(f'./users_data/{self.filename}', 'w') as file:
                file.write('')
                lines = []
        return lines

    def get_dates_from_file(self) -> list[str]:
        """
        Method to get dates of app usage from user's file
        :return: List of dates of every use of this app
        """
        lines = self.get_records()
        return list(map(lambda line: line.split('|')[0], lines))

    def get_bmi_from_file(self) -> list[str]:
        """
        Method to get bmis from user's file
        :return: List of user's recored bmis
        """
        lines = self.get_records()
        return [line.split('|')[-1].split(' ')[-1].strip() for line in lines]

    def get_height_from_file(self) -> list[str]:
        """
        Method to get height from user's file
        :return: List of user's recored heights
        """
        lines = self.get_records()
        return [line.split('|')[1].split(' ')[-1] for line in lines]

    def get_weight_from_file(self) -> list[str]:
        """
        Method to get weight from user's file
        :return: List of user's recored weights
        """
        lines = self.get_records()
        return [line.split('|')[2].split(' ')[-1] for line in lines]

    def last_record_person_instance(self) -> Person:
        """
        :return: Person instance out of user's records from file
        """
        return Person(float(self.get_height_from_file()[-1]), float(self.get_weight_from_file()[-1]))

    def get_last_date(self) -> date:
        """
        :return: date of last usage of this
        """
        lines = self.get_records()
        last_date = list(map(lambda x: int(x), lines[-1].split('|')[0].split('-')))
        return datetime(*last_date).date()

    def param_str(self) -> str:
        """
        :return: string of params so they can be saved into file
        """
        return '|'.join(self.params) + '\n'

    def save_to_file(self) -> None:
        """
        Method to save users' params into file.
        :return: None
        """
        if self.get_records():
            if self.get_last_date() == date.today():
                lines = self.get_records()
                with open(f'./users_data/{self.filename}', 'w') as file:
                    for line in lines[:-1]:
                        file.write(line)
        with open(f'./users_data/{self.filename}', 'a') as file:
            file.write(self.param_str())
