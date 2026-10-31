from src.exceptions.custom_exceptions import InvalidMarksError

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name
    @property
    def age(self):
        return self._age

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"

class Student(Person):
    def __init__(self,name, age, roll_number, study_hours, attendance, participation, total_score):
        super().__init__(name, age)
        self._roll_number = roll_number
        self._study_hours = study_hours
        self._attendance = attendance
        self._participation = participation
        self._total_score = total_score
        if self._total_score<0 or self._total_score>100:
            raise InvalidMarksError(self._total_score)
        if self._attendance<0 or self._attendance>100:
            raise InvalidMarksError(self._attendance)
    
    def calc_grade(self):
        thresholds = [(85, "A"), (70, "B"), (55, "C"), (40, "D")]
        return next(filter(lambda t: self._total_score >= t[0], thresholds), (0, "F"))[1]   
    
    def __str__(self):
        return f"Student: {self.name} | Roll: {self._roll_number} | Grade: {self.calc_grade()}"