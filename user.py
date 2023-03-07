from utilities import *

class Teacher():
    def __init__(self, email:str, password:str, name:str, firstname:str, tags_array: list = [], do_hash:bool = True) -> None:
        self.email = email.lower()
        if do_hash:
            self.password = hash(password)
        else:
            self.password = password
        self.name = name
        self.firstname = firstname
        self.tags_array = tags_array
    
    def add_tag(self, tag: str) -> bool:
        if tag not in self.tags_array:
            self.tags_array.append(tag)
            return True
        else:
            return False
    
    def remove_tag(self, tag: str) -> bool:
        if tag in self.tags_array:
            self.tags_array.pop(tag)
            return True
        else:
            return False

    def change_password(self, old_password, new_password) -> bool:
        if self.password == hash(old_password):
            self.password = hash(new_password)
            return True
        else:
            return False
    
    def get_registering_line(self) -> list:
        result = [self.email, self.password, self.name, self.firstname]
        if len(self.tags_array) > 0:
            tags_str = self.tags_array[0]
            for i in range(1, len(self.tags_array)):
                tags_str += ";" + self.tags_array[i]
            result.append(tags_str)
        else:
            result.append("")
        return result
    
class Student():
    def __init__(self, email:str, password:str, student_number: str, name:str, firstname:str, do_hash:bool = True) -> None:
        self.email = email.lower()
        if do_hash:
            self.password = hash(password)
        else:
            self.password = password
        self.student_number = student_number
        self.name = name
        self.firstname = firstname
    
    def change_password(self, old_password, new_password) -> bool:
        if self.password == hash(old_password):
            self.password = hash(new_password)
            return True
        else:
            return False
    
    def get_registering_line(self) -> list:
        result = [self.email, self.password, self.student_number, self.name, self.firstname]
        return result