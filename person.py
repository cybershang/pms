import uuid


class Person:
    def __init__(self) -> None:
        self._userid = uuid.uuid4()
        self._name = None
        self._sex = None
        self._salary = None

    @property
    def userid(self):
        return self._userid

    @userid.setter
    def userid(self):
        print("user id is imuutable!")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if len(name) == 0:
            print('Warning: name is empty!')
        self._name = name

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, sex: str):
        if sex not in ('male', 'female'):
            print("Warning: sex should be male or female")
        elif len(sex) == 0:
            print("Warning: sex is empty!")
        self._sex = sex

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, salary: float):
        if salary < 0:
            print('Fatal: salary can not be neganitive')
        else:
            self._salary = salary

    def __str__(self) -> str:
        return f"{self.userid}|{self.name}|{self.sex}|${self.salary}"
