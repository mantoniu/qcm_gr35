from utilities import *

class User():
    def __init__(self, email:str, password:str, name:str, firstname:str, tags_array: list = [], do_hash:bool = True) -> None: #firstname = prénom
        self.email = email
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