from utilities import *
from user import User

class UsersData():
    def __init__(self) -> None:
        self.users_array = list(User)
        csv_tab = read_csv("saves/users.csv")
        for row in csv_tab:
            self.users_array.append(User(row[0], row[1], row[2], row[3]))
    
    def containsUser(self, user: User) -> bool:
        for users in self.users_array:
            if(user.email == users[0]):
                return True
        return False

    def addUser(self, user: User) -> bool:
        if not(self.containsUser(user)):
            add_line_to_csv('saves/users.csv', [user.email, user.password, user.name, user.firstname])
            self.users.append(user)
            return True
        else:
            return False