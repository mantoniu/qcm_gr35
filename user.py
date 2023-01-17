from utilities import *

class User():
    def __init__(self, email:str, password:str, name:str, firstname:str) -> None: #firstname = prénom
        self.email = email
        self.password = hash(password)
        self.name = name
        self.firstname = firstname