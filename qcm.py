from markdown import markdown
from uuid import uuid4
from utilities import hash

class Question():
    def __init__(self, question: str, valids_reponses: list(int), possibles_responses: list(str), id: str = None) -> None:
        self.id = id
        self.question = question
        self.possibles_responses = possibles_responses
        self.valids_responses = valids_reponses

    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))
        return self.id

    def get_attributes(self):
        return {"question": self.question, "responses": self.possibles_responses}


class QCM:
    def __init__(self, name: str, questions_id: list, id:str = None) -> None:
        self.id = id
        self.name = name
        self.questions_id = questions_id
    
    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))
        return self.id