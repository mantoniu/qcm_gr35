from utilities import *
from user import User
from qcm import QCM, Statement

class UsersData():
    def __init__(self) -> None:
        self.users_array = []
        tab = read_file(create_save_file("saves/users.txt"))
        for row in tab:
            if len(row) > 4:
                self.users_array.append(User(email=row[0], password=row[1], name=row[2], firstname=row[3], tags_array=list(map(str, row[4].split(";"))), do_hash=False))
    
    def get_user_by_email(self, email) -> User:
        for users in self.users_array:
            if email == users.email:
                return users
        return None
    
    def contains_user(self, user: User) -> bool:
        return self.get_user_by_email(user.email) != None

    def add_user(self, user: User) -> bool:
        if not(self.contains_user(user)):
            add_line_to_file('saves/users.txt', user.get_registering_line())
            self.users_array.append(user)
            return True
        else:
            return False
    
    def add_tag_to_user_by_email(self, email: str, tag:str) -> bool:
        user = self.get_user_by_email(email)
        if user != None and user.add_tag(tag):
            set_lines_which_contains("saves/users.txt", email, user.get_registering_line())
            return True
        else:
            return False
    
    def remove_tag_to_user_by_email(self, email: str, tag: str) -> bool:
        user = self.get_user_by_email(email)
        if user != None and user.remove_tag(tag):
            set_lines_which_contains("saves/users.txt", email, user.get_registering_line())
            return True
        else:
            return False
    
    def login(self, email: str, password: str) -> bool:
        for users in self.users_array:
            if email == users.email:
                if hash(password) == users.password:
                    return True
                else:
                    return False
        return False

class StatementsData():
    def __init__(self) -> None:
        self.statements_array = []
        tab = read_file(create_save_file("saves/statements.txt"))
        for row in tab:
            if len(row) > 6:
                possibles_responses = []
                for i in range(6, len(row)):
                    possibles_responses.append(row[i])
                self.statements_array.append(Statement(id=row[0], name=row[1], question=row[2], valids_reponses=list(map(int, row[3].split(";"))), user_email=row[4], tags=list(map(str, row[5].split(";"))), possibles_responses=possibles_responses))

    def contains_id(self, id: str):
        for statements in self.statements_array:
            if statements.id == id:
                return True
        return False

    def contains_statement(self, statement: Statement) -> bool:
        return self.contains_id(statement.id)

    def add_statement(self, statement: Statement) -> None:
        add_line_to_file('saves/statements.txt', statement.get_registering_line())
        self.statements_array.append(statement)
    
    def remove_statement_with_id_in_file(self, id: str) -> None:
        remove_lines_which_contains("saves/statements.txt", id)
    
    def remove_statement(self, statement: Statement) -> None:
        self.statements_array.remove(statement)
        self.remove_statement_with_id_in_file(id=statement.id)
    
    def get_all_statements(self) -> list:
        return self.statements_array
    
    def get_statement_by_id(self, id: str) -> Statement:
        for statements in self.statements_array:
            if statements.id == id:
                return statements
        return None
    
    def get_statement_from_user(self, email) -> list:
        result = []
        for statements in self.statements_array:
            if statements.user_email == email:
                result.append(statements)
        return result
    
    def set_statement(self, id: str, new_statement: Statement) -> None:
        statement = self.get_statement_by_id(id)
        statement.set(new_statement=new_statement)
        set_lines_which_contains("saves/statements.txt", id, statement.get_registering_line())

class QCMData():
    def __init__(self, statements_data: StatementsData) -> None:
        self.statements_data = statements_data
        self.qcm_array = []
        tab = read_file(create_save_file("saves/qcm.txt"))
        for row in tab:
            if len(row) > 3:
                statements = []
                for i in range(3, len(row)):
                    statements.append(self.statements_data.get_statement_by_id(row[i]))
                self.qcm_array.append(QCM(id=row[0], name=row[1], user_email=row[2], statements=statements))
    
    def contains_id(self, id: str):
        for qcm in self.qcm_array:
            if qcm.id == id:
                return True
        return False
    
    def contains_qcm(self, qcm: QCM) -> bool:
        return self.contains_id(qcm.id)

    def add_qcm(self, qcm: QCM) -> None:
        add_line_to_file('saves/qcm.txt', qcm.get_registering_line())
        self.qcm_array.append(qcm)
    
    def get_all_qcm(self) -> list:
        return self.qcm_array
    
    def get_qcm_from_user(self, email: str) -> list:
        result = []
        for qcm in self.qcm_array:
            if qcm.user_email == email:
                result.append(qcm)
        return result
    
    def get_qcm_by_id(self, id: str) -> QCM:
        for qcm in self.qcm_array:
            if qcm.id == id:
                return qcm
        return None

def init():
    global users_data
    users_data = UsersData()
    global statements_data
    statements_data = StatementsData()
    global qcm_data
    qcm_data = QCMData(statements_data=statements_data)