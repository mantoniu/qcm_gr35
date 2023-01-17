
class Question():
    def __init__(self, question: str, possibles_responses: list(str), valids_reponses: list(int)) -> None:
        self.question = question
        self.possibles_responses = possibles_responses
        self.valids_responses = valids_reponses
    def get_display(self):
        return 


class QCM:
    def __init__(self, name: str, questions: list(Question)) -> None:
        self.name = name
        self.questions = questions
    def display():

        return 