from enum import Enum
     
class Task(Enum):
    NONE = 0,       # нет задачи 
    GET_LIST = 1,   # вывести список
    ADD = 2,        # новая заметка
    EDIT = 3,       # редактор
    GET = 4,        # прочитать заметку
    DELETE = 5      # удаление