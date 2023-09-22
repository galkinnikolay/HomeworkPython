
from tasks import Task
import json, os
from datetime import datetime

path = 'notes/'

def parse_datetime(string):
    try:
        result = datetime.strptime(string, "%m-%d-%Y %H:%M:%S")       
    except Exception:  
        return None
    return result                

def get_notes(date_min: datetime,   
              date_max: datetime):
    result = []
    list_names_item = os.listdir(path)
    for one in list_names_item:        
        if os.path.isfile(path + one):       
            try:                
                f = open(path + one, 'r', encoding='utf-8')
                note = json.load(f)

                note_datetime = parse_datetime(note['datetime'])
                if note_datetime == None: 
                    return None, 'ошибка данных: ' + note['datetime']  
                                
                if date_min != None: 
                    if note_datetime < date_min:   
                        continue
                if date_max != None: 
                    if note_datetime > date_max:   
                        continue
                result.append(note)
            except Exception:      
                return None, 'ошибка чтения файла: ' + path + one                
            finally:
                f.close()            
    return result, None  
    
def handler_files(task: Task,
                  title: str,
                  item: str, 
                  idNote: int):
    errorMessage = None
    if task == Task.ADD:
        note = {}        
        note['id'] = 0
            
        notes, errorMessage = get_notes(None, None)     
        if errorMessage != None:
            return  errorMessage
        
        # print(f'notes = {notes}')
        if len(notes) > 0:        
            id_max = 0
            for one in notes:
                if one['id'] > id_max:
                    id_max = one['id']      
            note['id'] = id_max + 1                   
        
        note['title'] = title
        note['item'] = item
        note['datetime'] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            
        namefile = str(note['id']) + '.json'
        try:
            with open(path + namefile, 'w', encoding='utf-8') as fw:
                json.dump(note, fw)                  
        except Exception :
            errorMessage = 'не удалось создать файл ' + namefile
            
    if task == Task.EDIT:  
        notes, errorMessage = get_notes(None, None)
        if errorMessage != None:
            return  errorMessage
        
        found = False
        for el in notes:
            if idNote == el['id']:
                el['item'] = item
                el['datetime'] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                namefile = str(idNote) + '.json'
                try:
                    with open(path + namefile, 'w', encoding='utf-8') as fw:
                        json.dump(el, fw)                  
                except Exception :
                    errorMessage = 'не удалось создать файл ' + namefile        
                found = True                    
                break    
        if not found:
            errorMessage = 'передан некорректный idNote = ' + str(idNote)            
            
    if task == Task.DELETE:            
        notes, errorMessage = get_notes(None, None)
        if errorMessage != None:
            return  errorMessage
        found = False
        for el in notes:
            if idNote == el['id']:
                namefile = str(idNote) + '.json'
                try:
                    os.remove(path + namefile)
                except Exception:
                    errorMessage = 'не удалось удалить файл ' + namefile        
                found = True                    
                break                       
                
        if not found:
            errorMessage = 'передан некорректный idNote = ' + str(idNote)                      
    return  errorMessage