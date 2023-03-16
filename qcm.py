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
    
class Reponse():
    def __init__(self) -> None:
        pass

class LiveQCM():
    def __init__(self, owner_email: str, statements: list, id: str = None, stats: list = [{}], opened: bool = True) -> None:
        self.owner_email = owner_email
        self.statements = statements
        self.students_email = []
        self.students_responses = stats
        self.statement_index = 0
        self.paused = False
        if id == None:
            self.generate_id()
        else:
            self.id = id
        self.opened = opened

    def has_responded(self, student_email: str) -> bool:
        students_dic = self.students_responses[self.statement_index]
        return student_email in students_dic and students_dic[student_email] != []

    def respond(self, student_email: str, responses: list) -> bool :
        if not(self.paused):
            if student_email in self.students_email and not(self.has_responded(student_email)):
                self.students_responses[self.statement_index][student_email] = responses
                return True
            else:
                return False
        else:
            return False
    
    def get_responses_from_student_email(self, student_email: str) -> list:
        responses = []
        for students_dic in self.students_responses:
            if student_email in students_dic:
                responses.append(students_dic[student_email])
            else:
                responses.append([])
        return responses
    
    def get_current_responses_from_student_email(self, student_email: str) -> list:
        if len(self.get_responses_from_student_email(student_email)) >= self.statement_index:
            return self.get_responses_from_student_email(student_email)[self.statement_index]
        else:
            return []

    def get_responses_count(self) -> list:
        responses_count = [0] * len(self.get_current_statement().possibles_responses)
        current_responses_from_all_students = self.students_responses[self.statement_index]
        for students_email in current_responses_from_all_students:
            one_student_responses_tab = current_responses_from_all_students[students_email]
            for responses in one_student_responses_tab:
                responses_count[responses] += 1
        return responses_count

    def get_total_responses_count(self) -> int:
        return len(self.students_responses[self.statement_index])


    def pause(self) -> bool:
        if not(self.paused):
            self.paused = True
            return True
        else:
            return False
    
    def resume(self) -> bool:
        if self.paused:
            self.paused = False
            return True
        else:
            return False
    
    def pause_or_resume(self) -> bool:
        if self.paused:
            self.paused = False
        else:
            self.paused = True
        return self.paused
    
    def is_paused(self) -> bool:
        return self.paused

    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))[:8]
        return self.id

    def end(self) -> bool:
        if self.opened:
            self.opened = False
            return True
        else:
            return False
    
    def get_current_statement(self) -> Statement:
        return self.statements[self.statement_index]
    
    def get_statements_len(self) -> int:
        return len(self.statements)

    def next_statement(self) -> bool:
        current_students_responses = self.students_responses[self.statement_index]
        students_who_responded = list(current_students_responses.keys())
        for students_email in self.students_email:
            if not(students_email in students_who_responded):
                current_students_responses[students_email] = []

        self.statement_index = self.statement_index + 1
        if self.statement_index >= self.get_statements_len():
            self.end()
            return True
        self.students_responses.append({})
        return False
    
    def get_students_count(self) -> int:
        return len(self.students_email)
    
    def contains_student(self, student_email: str) -> bool:
        for elements in self.students_email:
            if student_email == elements:
                return True
        return False
    
    def student_join(self, email: str) -> bool:
        if not(email in self.students_email):
            self.students_email.append(email)
            for students_dic in self.students_responses:
                if not(email in students_dic):
                    students_dic[email] = []
            return True
        else:
            return False

    def student_leave(self, email: str) -> bool:
        if email in self.students_email:
            self.students_email.remove(email)
            return True
        else:
            return False
    
    def get_registering_line(self) -> list:
        line_to_add = [self.id, self.owner_email]
        statements_str = self.statements[0].id
        for i in range(1, self.get_statements_len()):
            statements_str += ";" + self.statements[i].id
        line_to_add.append(statements_str)
        for statements_dic in self.students_responses:
            row_to_add = ""
            for keys in statements_dic:
                row_to_add += keys + ":"
                if len(statements_dic[keys]) > 0:
                    row_to_add += str(statements_dic[keys][0])
                    for i in range(1, len(statements_dic[keys])):
                        row_to_add += ";" + str(str(statements_dic[keys][i]))
                row_to_add += ","
            row_to_add = row_to_add[:-1]
            line_to_add.append(row_to_add)
            

        return line_to_add

    def __eq__(self, other_liveqcm : LiveQCM) -> bool:
        return self.statements == other_liveqcm.statements