from utilities import *

class User():
    def __init__(self, email:str, password:str, name:str, firstname:str, do_hash:bool = True) -> None: #firstname = prénom
        self.email = email
        if do_hash:
            self.password = hash(password)
        else:
            self.password = password
        self.name = name
        self.firstname = firstname
    
    def __repr__(self) -> str:
        return self.email + ";" + self.password + ";" + self.name + ";" + self.firstname