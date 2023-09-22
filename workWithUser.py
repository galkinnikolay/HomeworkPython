from tasks import Task
from workWithFiles import *

class WorkWithUser:
    def __init__(self):
        self.task: Task = Task.NONE       
        self.idNote: int = None    
        self.title: str = None        
        self.item: str = None         
        self.datetime_min: datetime = None
        self.datetime_max: datetime = None

    def initial_state(self):
        self.task = Task.NONE       
        self.idNote = None       
        self.title = None       
        self.item = None        
        self.datetime_min = None   
        self.datetime_max = None

    def parse_string_datetime_limits(self, string):
        splitted = string.split(',')
        if len(splitted) != 2:
            return 'сплит по запятой должен дать 2 элемента'

        parsed_left = splitted[0].strip()
        if parsed_left.lower() == 'no':
            self.datetime_min = None
        else:
            result = parse_datetime(parsed_left)
            if result == None: 
                return 'не спарсено выражение ' + parsed_left
            self.datetime_min = result

        parsed_right = splitted[1].strip()
        if parsed_right.lower() == 'no':
            self.datetime_max = None
        else:
            result = parse_datetime(parsed_right)
            if result == None:
                return 'не спарсено выражение ' + parsed_right
            self.datetime_max = result
        if self.datetime_min != None and self.datetime_max != None and self.datetime_min > self.datetime_max:
            return 'некооректно заданы границы: нижняя превышает верхнюю'
        return None

    def print_offer(self):
        if self.task == Task.NONE:  
            print('\nВыберите операцию:')
            print('1. Вывести список заметок')
            print('2. Создать новую заметку')
            print('3. Отредактировать заметку')
            print('4. Просмотреть заметку')
            print('5. Удалить заметку')

        elif self.task == Task.GET_LIST:
            print('Для формирования выборки заметок укажите границы дат слева и справа, через запятую в формате "%m-%d-%Y %H:%M:%S"')
            print("Если дата не установлена, введите 'no'")
            print('Примеры: 08-01-2023 17:47:35, 08-10-2023 23:59:59')
            print('         no, 08-10-2023 23:59:59')
            print('         no, no  (будут выведены все заметки)')

        elif self.task == Task.ADD: 
            if self.title == None:
                print('Введите название заметки:')
            else:
                print('Введите текст заметки:')

        elif self.task == Task.EDIT:   
            if self.idNote == None:
                print(
                    'Введите id заметки для редактирования. Посмотреть id заметок можно в выборе п.1')
            else:
                print('введите новое содержимое заметки:')

        elif self.task == Task.GET:  
            print('Введите id заметки для просмотра. Посмотреть id заметок можно в выборе п.1')

        elif self.task == Task.DELETE: 
            print('Введите id заметки для удаления. Посмотреть id заметок можно в выборе п.1')

    def handler_message_user(self, message_user):
        if message_user == '':
            print('Введена пустая строка')
            return

        if self.task == Task.NONE:
            if message_user == '1':
                self.task = Task.GET_LIST
            elif message_user == '2':
                self.task = Task.ADD
            elif message_user == '3':
                self.task = Task.EDIT
            elif message_user == '4':
                self.task = Task.GET
            elif message_user == '5':
                self.task = Task.DELETE
            else:
                print('Некорректный ввод')

        elif self.task == Task.GET_LIST:
            errorMessage = self.parse_string_datetime_limits(message_user)
            if errorMessage != None:
                print('Ошибка ввода данных: ' + errorMessage)
            else:
                list_notes, errorMessage = get_notes(self.datetime_min, self.datetime_max)
                if errorMessage != None:
                    print('Ошибка get_notes: ' + errorMessage)
                else:
                    if len(list_notes) == 0:
                        print('заметок нет')
                    else:
                        print('Список заметок (отсортирован по id):')
                        for el in list_notes:
                            print(
                                f"id:{el['id']}, '{el['title']}', создана: {el['datetime']}")
                self.initial_state()     

        elif self.task == Task.ADD:  
            if self.title == None:
                self.title = message_user
            else:
                self.item = message_user

                errorMessage = handler_files(self.task, self.title, self.item, self.idNote)
                if errorMessage == None:
                    print('заметка успешно создана')
                    self.initial_state()      
                else:
                    print(errorMessage)

        elif self.task == Task.EDIT:    
            list_notes, errorMessage = get_notes(None, None)
            if errorMessage != None:
                print('Ошибка get_notes: ' + errorMessage)
            else:
                if self.idNote == None:
                    for el in list_notes:
                        if message_user == str(el['id']):
                            self.idNote = el['id']
                            print(f'Выбранная заметка: id = {self.idNote}')
                            print(f"Заголовок(название): {el['title']}")
                            print(f"Содержимое: {el['item']}")
                            print(f"Дата-время создания: {el['datetime']}")
                            break
                    if self.idNote == None:
                        print('Неверно указан id')
                else:
                    self.item = message_user

                    errorMessage = handler_files(self.task, self.title, self.item, self.idNote)
                    if errorMessage == None:
                        print('заметка успешно отредактирована')
                        self.initial_state()    
                    else:
                        print(errorMessage)

        elif self.task == Task.GET:
            list_notes, errorMessage = get_notes(None, None)
            if errorMessage != None:
                print('Ошибка get_notes: ' + errorMessage)
            else:
                found = False
                for el in list_notes:
                    if message_user == str(el['id']):
                        print('Выбранная заметка: id = ' + message_user)
                        print(f"Заголовок(название): {el['title']}")
                        print(f"Содержимое: {el['item']}")
                        print(f"Дата-время создания: {el['datetime']}")

                        self.initial_state()
                        found = True
                        break
                if not found:
                    print('Неверно указан id')

        elif self.task == Task.DELETE:
            list_notes, errorMessage = get_notes(None, None)
            if errorMessage != None:
                print('Ошибка get_notes: ' + errorMessage)
            else:
                found = False
                for el in list_notes:
                    if message_user == str(el['id']):
                        found = True
                        self.idNote = el['id']

                        errorMessage = handler_files(self.task, self.title, self.item, self.idNote)
                        if errorMessage == None:
                            print('заметка успешно удалена')
                            self.initial_state()  
                        else:
                            print(errorMessage)
                        break
                if not found:
                    print('Неверно указан id')