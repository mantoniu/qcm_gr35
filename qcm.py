from __future__ import annotations
from markdown import markdown
from uuid import uuid4
from utilities import hash, file_contains
from user import Student, Teacher

md_extensions = ['md_mermaid','markdown.extensions.attr_list','markdown.extensions.codehilite','markdown.extensions.fenced_code']

class Statement():
    def __init__(self, name: str, question: str, valids_reponses: list, possibles_responses: list, user_email: str, id: str = None, tags: list = []) -> None:
        self.name = name
        self.question = question
        self.possibles_responses = possibles_responses
        self.valids_responses = valids_reponses
        self.user_email = user_email
        self.tags = tags
        self.decimal = len(possibles_responses)==1

        if id == None:
            self.generate_id()
        else:
            self.id = id

    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))[:8]
        return self.id

    def get_state(self) -> markdown:
        return markdown("\n"+self.question,extensions=md_extensions)
    
    def set(self, new_statement: Statement) -> None:
        self.name = new_statement.name
        self.question = new_statement.question
        self.possibles_responses = new_statement.possibles_responses
        self.valids_responses = new_statement.valids_responses
        self.user_email = new_statement.user_email
        self.tags = new_statement.tags
        self.decimal = len(new_statement.possibles_responses)==1
    
    def get_registering_line(self) -> list:
        line_to_add = [self.id, self.name, self.question]
        valids_responses_indexes = ""
        if len(self.valids_responses) > 0:
            valids_responses_indexes += str(self.valids_responses[0])
            for i in range(1, len(self.valids_responses)):
                valids_responses_indexes += ";" + str(self.valids_responses[i])
        line_to_add.append(valids_responses_indexes)
        line_to_add.append(self.user_email)
        tags = ""
        if len(self.tags) > 0:
            tags += str(self.tags[0])
            for i in range(1, len(self.tags)):
                tags += ";" + str(self.tags[i])
        line_to_add.append(tags)
        for responses in self.possibles_responses:
            line_to_add.append(responses)
        return line_to_add

    def is_projected(self, liveqcms : list) -> bool:
      for liveqcm in liveqcms:
            for statements in liveqcm.statements:
                  if self == statements:
                        return True
      return False


    def __eq__(self, stmt: Statement) -> bool:
        return self.id == stmt.id


class QCM:
    def __init__(self, name: str, statements: list, user_email: str, id:str = None) -> None:
        self.name = name
        self.statements = statements
        self.user_email = user_email
        if id == None:
            self.generate_id()[:8]
        else:
            self.id = id
    
    def add_statement(self, statement: Statement) -> None:
        self.statements.append(statement)
    
    def remove_statement(self, statement: Statement) -> None:
        for i in range(len(self.statements)):
            if self.statements[i].id == statement.id:
                self.statements.pop(i)
    
    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))
        return self.id
    
    def get_registering_line(self) -> list:
        line_to_add = [self.id, self.name, self.user_email]
        for statement in self.statements:
            line_to_add.append(statement.id)
        return line_to_add

    def is_projected(self, liveqcms : list) -> bool:
      for liveqcm in liveqcms:
            if liveqcm.statements == self.statements:
                return True
      return False


## Ajouter sauvegarde

class LiveQCM():
    def __init__(self, owner_email: str, statements: list, id: str = None, opened: bool = True, owner_sid: str = None) -> None:
        self.owner_email = owner_email
        self.owner_sid = owner_sid
        self.statements = statements
        self.statements_len = len(statements)
        self.connected_sockets_ids = {}
        self.students_responses = []
        self.statement_index = 0
        if id == None:
            self.generate_id()
        else:
            self.id = id
        self.opened = opened

    def respond(self, student_id: str, responses: list) -> bool :
        if student_id in self.get_students():
            self.students_responses[self.question_index][student_id] = responses
            return True
        else:
            return False
    
    def get_responses_from_student_id(self, student_id: str) -> list:
        responses = []
        for students_dic in self.students_responses:
            if student_id in students_dic:
                responses.append(students_dic[student_id])
            else:
                responses.append([])
        return responses

    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))[:8]
        return self.id

    def end(self) -> bool:
        if self.opened:
            self.opened = False
            return True
        else:
            return False

    def next_question(self) -> bool:
        self.question_index = self.question_index + 1
        if self.question_index >= self.statements_len:
            self.end()
            return True
        return False

    def get_students(self) -> list:
        return self.connected_sockets_ids.values()
    
    def get_students_count(self) -> int:
        return len(self.connected_sockets_ids)
    
    def student_join(self, student_id: str, socket_id: str) -> bool:
        if not(student_id in self.get_students()):
            self.connected_sockets_ids[socket_id] = student_id
            return True
        else:
            return False

    def student_leave(self, student_id: str) -> str:
        if student_id in self.get_students():
            for keys in self.connected_sockets_ids:
                if self.connected_sockets_ids[keys] == student_id:
                    self.connected_sockets_ids.pop(keys)
                    return keys
            return None
        else:
            return None
    
    def get_registering_line(self) -> list:
        line_to_add = [self.id, self.owner_email]
        for statement in self.statements:
            line_to_add.append(statement.id)
        return line_to_add

    def __eq__(self, other_liveqcm : LiveQCM) -> bool:
        return self.statements == other_liveqcm.statements