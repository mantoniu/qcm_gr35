from markdown import markdown
from uuid import uuid4
from utilities import hash

md_extensions = ['md_mermaid','markdown.extensions.attr_list','markdown.extensions.codehilite','markdown.extensions.fenced_code']

class Question():
    def __init__(self, question: str, valids_reponses: list, possibles_responses: list, user_email: str, id: str = None) -> None:
        self.id = id
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
    def __init__(self, name: str, questions: list, user_email: str, id:str = None) -> None:
        self.id = id
        self.name = name
        self.questions = questions
        self.user_email = user_email
    
    def add_question(self, question: Question) -> None:
        self.questions.append(question)
    
    def remove_question(self, question: Question) -> None:
        for i in range(len(self.questions)):
            if self.questions[i].id == question.id:
                self.questions.pop(i)
    
    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))
        return self.id