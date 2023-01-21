from utilities import *
from user import User
from qcm import QCM, Statement

class UsersData():
    def __init__(self) -> None:
        self.users_array = []
        tab = read_file(create_save_file("users.txt"))
        for row in tab:
            if len(row) > 3:
                self.users_array.append(User(email=row[0], password=row[1], name=row[2], firstname=row[3], do_hash=False))
    
    def containsUser(self, user: User) -> bool:
        for users in self.users_array:
            if user.email == users.email:
                return True
        return False

    def addUser(self, user: User) -> bool:
        if not(self.containsUser(user)):
            add_line_to_file('saves/users.txt', [user.email, user.password, user.name, user.firstname])
            self.users_array.append(user)
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
        tab = read_file(create_save_file("statements.txt"))
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
        id = statement.generate_id()
        while id == "" or self.contains_id(id):
            id = statement.generate_id()
        line_to_add = [statement.id, statement.name, statement.question]
        valids_responses_indexes = []
        if len(valids_responses_indexes) > 0:
            valids_responses_indexes.append(str(statement.valids_responses[0]))
            for i in range(1, len(statement.valids_responses)):
                valids_responses_indexes += ";" + str(statement.valids_responses[i])
        line_to_add.append(valids_responses_indexes)
        line_to_add.append(statement.user_email)
        tags = []
        if len(tags) > 0:
            tags.append(str(statement.tags[0]))
            for i in range(1, len(statement.tags)):
                tags += ";" + str(statement.valids_responses[i])
        line_to_add.append(tags)
        for responses in statement.possibles_responses:
            line_to_add.append(responses)
        add_line_to_file('saves/statements.txt', line_to_add)
        self.statements_array.append(statement)
    
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

class QCMData():
    def __init__(self, statements_data: StatementsData) -> None:
        self.statements_data = statements_data
        self.qcm_array = []
        tab = read_file(create_save_file("qcm.txt"))
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
        id = qcm.generate_id()
        while id == "" or self.contains_id(id):
            id = qcm.generate_id()
        line_to_add = [qcm.id, qcm.name, qcm.user_email]
        for statements in qcm.statements: # Attention à ça
            self.statements_data.add_statement(statements)
            line_to_add.append(statements.question)
        add_line_to_file('saves/qcm.txt', line_to_add)
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