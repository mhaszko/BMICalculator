class Person:
    """
    Class Person used to create objects describing parameters of persons using the BMI calculator.
    """
    def __init__(self, height, weight, ):
        self.height = height
        self.weight = weight

    def calculate_bmi(self):
        return round(self.weight / self.height ** 2, 2)

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


class Sportsman(Person):
