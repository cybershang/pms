import sqlite3
from person import Person
from pathlib import Path
import csv
import pandas
import webbrowser


class Manager:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('my.db')
        self.cursor = self.connection.cursor()
        self._tables = None
        self._menu = None
        self.func_dict = {1: self.add_person, 2: self.remove_person,
                          3: self.modify_person, 4: self.search_person, 5: self.show, 6: self.export}

    def init_db(self):
        self.tables = 'get table list from file'
        if self.tables is None:
            self.cursor.execute(
                '''CREATE TABLE person(userid TEXT, personal_name TEXT, sex TEXT, salary REAL);''')
            print('table person created successfully!')
        else:
            print('detect exist table person')

    @property
    def tables(self):
        return self._tables

    @tables.setter
    def tables(self, talbes):
        self.cursor.execute(
            '''SELECT name FROM sqlite_master WHERE type='table';''')
        try:
            self._tables = list(self.cursor.fetchall()[0])
        except IndexError:  # TODO: may better solution exist?
            pass

    @property
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, defined_menu: str):
        self._menu = defined_menu

    def get_person(self, userid: str):
        try:
            self.cursor.execute(
                f'''SELECT * FROM person WHERE userid = "{userid}"''')
            user = self.cursor.fetchall()
        except sqlite3.OperationalError as err:
            if 'no such column' in str(err):
                return None
        else:
            return user[0]

    def search_person(self):
        userid = input('userid:')
        user = self.get_person(userid)
        if user is not None:
            print(user)
        else:
            print(f'user:{userid} is not exist!')

    def add_person(self):
        person = Person()
        person.name = input('name:')
        person.sex = input('sex:')
        try:
            person.salary = float(input('salary:'))
        except ValueError:
            print('Fatal: salary should be digit')
        value = f'"{person.userid}","{person.name}", "{person.sex}", "{person.salary}"'

        self.cursor.execute(f'''INSERT INTO person VALUES ({value})''')

    def remove_person(self):
        userid = input('userid:')
        user = self.get_person(userid)
        if user is not None:
            print(
                f'you want delete\nid: {user[0]}\nname: {user[1]}\nsex: {user[2]}\nsalary: {user[3]}')
            if input('are you sure? y/n:') == 'y':
                self.cursor.execute(
                    f'''DELETE FROM person WHERE userid = "{userid}";''')
                self.connection.commit()
                print('delete successfully!')

    def modify_person(self):
        def modify_personal_name(name: str):
            self.cursor.execute(
                f'''UPDATE person SET personal_name={name} WHERE userid="{userid}"";''')

        def modify_sex(sex: str):
            self.cursor.execute(
                f'''UPDATE person SET sex={sex} WHERE userid="{userid}";''')

        def modify_salary(salary: float):
            self.cursor.execute(
                f'''UPDATE person SET salary={salary} WHERE userid="{userid}";''')

        userid = input('userid:')
        user = self.get_person(userid)
        if user is not None:
            print(
                f'you want modify\nid: {user[0]}\nname: {user[1]}\nsex: {user[2]}\nsalary: {user[3]}')

            if input('are you sure? y/n:') == 'y':
                personal_name = input('name:')

                if personal_name == ' ':
                    modify_personal_name('')
                elif personal_name != '':
                    modify_personal_name(personal_name)

                sex = input('sex:')
                if sex == ' ':
                    modify_sex('')
                elif sex != '':
                    modify_sex(sex)

                salary = input('salary:')
                if (salary == ' ') or (salary == '0'):
                    modify_salary(0)
                elif salary != '':
                    modify_salary(float(salary))

    def show(self):
        def output_cmd():
            print('id|name|sex|salary')
            self.cursor.execute('''SELECT * FROM person''')
            for row in self.cursor.fetchall():
                print('|'.join(str(field) for field in row))

        def present_on_broswer():
            person_csv = Path('person.csv')
            if person_csv.is_file() is False:
                self.export()
            pandas.read_csv("person.csv").to_html('table.html')
            modify_style()
            webbrowser.open("table.html")

        def modify_style():
            with open('table.html', 'r') as f:
                code = f.read()
            with open('table.html', 'w') as f:
                code = code.replace('''<tr style="text-align: right;">''',
                                    '''<tr style="text-align: center;">''')
                f.write(code)

        output_cmd()
        present_on_broswer()

    def export(self):
        self.cursor.execute('''SELECT * FROM person''')
        with open('person.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'sex', 'salary'])
            for row in self.cursor.fetchall():
                row = list(row)
                row[-1] = str(row[-1])
                writer.writerow(row)
                print(row)
        print('person.csv saved!')
