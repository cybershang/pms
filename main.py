from person import Person
from manage import Manager
import sqlite3


def main():
    manager = Manager()
    manager.menu = '1.add\n2.remove\n3.modify\n4.search\n5.show\n6.export\n7.exit'
    manager.init_db()
    while True:
        print(manager.menu)
        try:
            try:
                choice = int(input('function:'))
            except ValueError:
                print('please input in 1-6')
            else:
                if choice == 7:
                    manager.connection.commit()
                    manager.connection.close()
                    print('all changes save!')
                    exit(0)
                try:
                    manager.func_dict[choice]()
                except KeyError:
                    print('please input in 1-5')
        except KeyboardInterrupt:
            manager.connection.commit()
            manager.connection.close()
            print('\nall changes saved!')
            exit(0)


if __name__ == '__main__':
    main()

