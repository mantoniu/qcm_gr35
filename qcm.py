from __future__ import annotations
from markdown import markdown
from uuid import uuid4
from utilities import hash, file_contains

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
        self.id = hash(str(uuid4()))
        return self.id

    def get_state(self) -> markdown:
        return markdown("\n"+self.question,extensions=md_extensions)
    
    def set(self, new_statement: Statement):
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


class QCM:
    def __init__(self, name: str, statements: list, user_email: str, id:str = None) -> None:
        self.name = name
        self.statements = statements
        self.user_email = user_email
        if id == None:
            self.generate_id()
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
    
    def get_registering_line(self):
        line_to_add = [self.id, self.name, self.user_email]
        for statement in self.statements:
            line_to_add.append(statement.id)
        return line_to_add