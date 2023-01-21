from markdown import markdown
from uuid import uuid4
from utilities import hash

md_extensions = ['md_mermaid','markdown.extensions.attr_list','markdown.extensions.codehilite','markdown.extensions.fenced_code']

class Statement():
    def __init__(self, name: str, tags : str, question: str, valids_reponses: list, possibles_responses: list, user_email: str, id: str = None) -> None:
        self.name = name
        self.id = id
        self.tags = tags
        self.question = question
        self.possibles_responses = possibles_responses
        self.valids_responses = valids_reponses
        self.user_email = user_email

    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))
        return self.id

    def get_state(self) -> markdown:
        return markdown(self.question,extensions=md_extensions)


class QCM:
    def __init__(self, name: str, statements: list, user_email: str, id:str = None) -> None:
        self.id = id
        self.name = name
        self.statements = statements
        self.user_email = user_email
    
    def add_statement(self, statement: Statement) -> None:
        self.statements.append(statement)
    
    def remove_statement(self, statement: Statement) -> None:
        for i in range(len(self.statements)):
            if self.statements[i].id == statement.id:
                self.statements.pop(i)
    
    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))
        return self.id