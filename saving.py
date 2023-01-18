from utilities import *
from user import User
from qcm import QCM, Question

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

class QuestionsData():
    def __init__(self) -> None:
        self.questions_array = []
        tab = read_file(create_save_file("questions.txt"))
        for row in tab:
            if len(row) > 3:
                possibles_responses = []
                for i in range(3, len(row)):
                    possibles_responses.append(row[i])
                self.questions_array.append(Question(id=row[0], question=row[1], valids_reponses=list(map(int, row[2].split(";"))), possibles_responses=possibles_responses))
    
    def contains_id(self, id: str):
        for questions in self.questions_array:
            if questions.id == id:
                return True
        return False

    def contains_question(self, question: Question) -> bool:
        return self.contains_id(question.id)

    def add_question(self, question: Question) -> None:
        id = question.generate_id()
        while id == "" or self.contains_id(id):
            id = question.generate_id()
        line_to_add = [question.id, question.question]
        valids_responses_indexes = str(question.valids_responses[0])
        for i in range(1, len(question.valids_responses)):
            valids_responses_indexes += ";" + str(question.valids_responses[i])
        line_to_add.append(valids_responses_indexes)
        for responses in question.possibles_responses:
            line_to_add.append(responses)
        add_line_to_file('saves/questions.txt', line_to_add)
        self.questions_array.append(question)
    
    def get_all_questions(self) -> list:
        return self.questions_array
    
    def get_question_by_id(self, id: str) -> Question:
        for questions in self.questions_array:
            if questions.id == id:
                return questions
        return None

class QCMData():
    def __init__(self, questions_data: QuestionsData) -> None:
        self.questions_data = questions_data
        self.qcm_array = []
        tab = read_file(create_save_file("qcm.txt"))
        for row in tab:
            if len(row) > 2:
                questions = []
                for i in range(2, len(row)):
                    questions.append(self.questions_data.get_question_by_id(row[i]))
                self.qcm_array.append(QCM(id=row[0], name=row[1], questions=questions))
    
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
        line_to_add = [qcm.id, qcm.name]
        for questions in qcm.questions:
            self.questions_data.add_question(questions)
            line_to_add.append(questions.question)
        add_line_to_file('saves/qcm.txt', line_to_add)
        self.qcm_array.append(qcm)
    
    def get_all_qcm(self) -> list:
        return self.qcm_array

def init():
    global users_data
    users_data = UsersData()
    global questions_data
    questions_data = QuestionsData()
    global qcm_data
    qcm_data = QCMData(questions_data=questions_data)