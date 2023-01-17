from utilities import *
from user import User

class UsersData():
    def __init__(self) -> None:
        self.users_array = []
        tab = read_file("saves/users.txt")
        for row in tab:
            if len(row) > 3:
                self.users_array.append(User(row[0], row[1], row[2], row[3]))
    
    def containsUser(self, user: User) -> bool:
        for users in self.users_array:
            if(user.email == users.email):
                return True
        return False

    def addUser(self, user: User) -> bool:
        if not(self.containsUser(user)):
            add_line_to_file('saves/users.txt', [user.email, user.password, user.name, user.firstname])
            self.users_array.append(user)
            return True
        else:
            return False