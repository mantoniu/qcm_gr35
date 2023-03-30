from __future__ import annotations
from markdown import markdown
from uuid import uuid4
from utilities import hash,get_corrected_word
from time import time
from datetime import datetime

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
        self.open_question = len(possibles_responses)==0

        if id == None:
            self.generate_id()
        else:
            self.id = id

    def check_validity(self, responses: list) -> bool:
        return responses.sort() == self.valids_responses.sort()

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
        self.open_question = len(new_statement.possibles_responses) == 0
    
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


class QCM():
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

class LiveStatementStats():
    def __init__(self, stats : dict = {}, id: str = None, start_time: float = -1, end_time: float = -1, joins_leaves: list = []) -> None:
        self.stats = stats
        if id == None:
            self.generate_id()
        else:
            self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.joins_leaves = joins_leaves
    
    def start(self):
        self.start_time = time() + 3600
    
    def end(self):
        self.end_time = time() + 3600
    
    def join(self, student_email: str):
        last_index = -1
        for i in range(len(self.joins_leaves)):
            if self.joins_leaves[i][0] == student_email:
                last_index = i

        if last_index != -1 and time() - 0.3 < self.joins_leaves[last_index][1]:
            del self.joins_leaves[last_index]
        else:
            self.joins_leaves.append((student_email, time() + 3600))
    
    def leave(self, student_email: str):
        self.joins_leaves.append((student_email, time() + 3600))
    
    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))
        return self.id
    
    def get_all_students_responses(self) -> dict:
        return_dic = {}
        for students_email in self.stats:
            responses = list(map(str, self.stats[students_email]["responses"]))
            time = datetime.fromtimestamp(self.stats[students_email]["time"])
            validity = self.stats[students_email]["validity"]
            return_dic[students_email] = {"responses" : responses, "time" : time, "validity" : validity}
        return return_dic
    
    def get_students_responses(self) -> dict:
        students_responses = {}
        for students_emails in self.stats:
            students_responses[students_emails] = self.stats[students_emails]["responses"]
        return students_responses
    
    def get_one_student_responses(self, student_email: str) -> list:
        if student_email in self.stats:
            return self.stats[student_email]["responses"]
        else:
            return []
    
    def contains_student(self, student_email: str) -> bool:
        if student_email in self.stats:
            return True
        else:
            return False
    
    def set_response(self, student_email: str, responses: list, validity: bool) -> None:
        self.stats[student_email] = {"responses": responses, "time": time() + 3600, "validity": validity}
    
    def clear_responses(self):
        self.stats = {}
    
    def get_registering_line(self) -> str:
        start_time_str = str(self.start_time)
        end_time_str = str
        if self.end_time != -1:
            end_time_str = str(self.end_time)
        else:
            max_time = 0
            for students in self.stats:
                if self.stats[students]["time"] > max_time:
                    max_time = self.stats[students]["time"]
            end_time_str = str(max_time)
        line_to_add = [self.id, start_time_str, end_time_str]
        stats_str = ""
        if len(self.stats) > 0:
            for students_email in self.stats:
                responses_str = ','.join(map(str, self.stats[students_email]["responses"]))
                time_str = str(self.stats[students_email]["time"])
                validity_str = str(self.stats[students_email]["validity"])
                stats_str += f"{students_email}:{responses_str}:{time_str}:{validity_str};"
            stats_str = stats_str[:-1]
        line_to_add.append(stats_str)
        if len(self.joins_leaves) > 0:
            joins_leaves_str = self.joins_leaves[0][0] + ":" + str(self.joins_leaves[0][1])
            for i in range(1, len(self.joins_leaves)):
                joins_leaves_str += ";" + self.joins_leaves[i][0] + ":" + str(self.joins_leaves[i][1])
            line_to_add.append(joins_leaves_str)
        else:
            line_to_add.append("")
        return line_to_add
    
    def __str__(self) -> str:
        return str(self.stats) + "===" + self.id

class LiveQCM():
    def __init__(self, owner_email: str, statements: list, id: str = None, stats: list = None, opened: bool = True) -> None:
        self.owner_email = owner_email
        self.statements = statements
        self.students_email = []
        self.stats = []
        self.word_dict = {}
        if stats == None:
            for i in range(len(statements)):
                livestatementstats = LiveStatementStats()
                self.stats.append(livestatementstats)
                livestatementstats.clear_responses()
        else:
            self.stats = stats
        self.statement_index = 0
        self.paused = False
        if id == None:
            self.generate_id()
        else:
            self.id = id
        self.opened = opened
        self.stats[0].start()
    
    def debug(self):
        to_print = ""
        for elements in self.stats:
            to_print += "\n" + str(elements) + "=" + hex(id(elements)) + "=" + elements.id + " "
        print(to_print)

    def has_responded(self, student_email: str) -> bool:
        students_dic = self.stats[self.statement_index].get_students_responses()
        return student_email in students_dic and students_dic[student_email] != []


    def respond(self, student_email: str, responses: list) -> bool :
        if not(self.paused):
            if student_email in self.students_email and not(self.has_responded(student_email)):    
                if self.get_current_statement().open_question:
                    new_word = get_corrected_word(responses[0])
                    if len(self.word_dict)==0:
                        self.word_dict[new_word] = 1
                    else:
                        for word in list(self.word_dict.keys()):
                            if word == new_word:
                                self.word_dict[new_word] += 1
                            else:
                                self.word_dict[new_word] = 1
                    self.stats[self.statement_index].set_response(student_email, [], True)
                    for i in range(self.statement_index + 1, len(self.stats)):
                        self.stats[i].clear_responses()
                    return True
                else:
                    validity = self.statements[self.statement_index].check_validity(responses)
                    self.stats[self.statement_index].set_response(student_email, responses, validity)
                    for i in range(self.statement_index + 1, len(self.stats)):
                        self.stats[i].clear_responses()
                    return True
        return False
    
    def get_reponses_by_time_xy(self) -> tuple:
        x_values = list(range(1, len(self.stats)+1))
        y_values = []
        for stat in self.stats:
            y_values.append(len(stat.stats))
        return (x_values, y_values)
    
    def get_logs(self) -> list:
        logs = []
        for stat in self.stats:
            logs.append(stat.get_all_students_reponses())
        return logs
    
    def get_responses_from_student_email(self, student_email: str) -> list:
        responses = []
        for all_stats in self.stats:
            responses.append(all_stats.get_one_student_responses(student_email))
        return responses
    
    def get_current_responses_from_student_email(self, student_email: str) -> list:
        if len(self.get_responses_from_student_email(student_email)) >= self.statement_index:
            return self.get_responses_from_student_email(student_email)[self.statement_index]
        else:
            return []

    def get_responses_count(self) -> list:
        responses_count = [0] * len(self.get_current_statement().possibles_responses)
        current_responses_from_all_students = self.stats[self.statement_index].get_students_responses()
        for students_email in current_responses_from_all_students:
            one_student_responses_tab = current_responses_from_all_students[students_email]
            for responses in one_student_responses_tab:
                responses_count[responses] += 1
        return responses_count

    def get_total_responses_count(self) -> int:
        return len(self.stats[self.statement_index].get_students_responses())


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
        print(str(self.statement_index) + " " + str(self.statements))
        return self.statements[self.statement_index]
    
    def get_statements_len(self) -> int:
        return len(self.statements)

    def next_statement(self) -> bool:
        self.word_dict = {}
        self.stats[self.statement_index].end()
        self.statement_index = self.statement_index + 1
        if self.statement_index >= self.get_statements_len():
            self.end()
            return True
        else:
            self.stats[self.statement_index].start()
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
            self.stats[self.statement_index].join(email)
            return True
        else:
            return False

    def student_leave(self, email: str) -> bool:
        if email in self.students_email:
            self.students_email.remove(email)
            self.stats[self.statement_index].leave(email)
            return True
        else:
            return False
    
    def get_registering_line(self) -> list:
        line_to_add = [self.id, self.owner_email]
        statements_str = self.statements[0].id
        stats_str = self.stats[0].id
        for i in range(1, self.get_statements_len()):
            statements_str += ";" + self.statements[i].id
            stats_str += ";" + self.stats[i].id
        line_to_add.append(statements_str)
        line_to_add.append(stats_str)
            
        return line_to_add

    def __eq__(self, other_liveqcm : LiveQCM) -> bool:
        if other_liveqcm == None:
            return False
        else:
            return self.statements == other_liveqcm.statements

class Test():
    def __init__(self, qcms_attribution: dict, owner_email: str, id:str = None) -> None:
        self.qcms_attribution = qcms_attribution
        self.owner_email = owner_email
        if id == None:
            self.generate_id()
        else:
            self.id = id

    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))
        return self.id
    
    def attribute_qcms(self, students_emails: list) -> bool:
        qcms_len = self.get_qcms_len()
        if qcms_len == len(students_emails):
            values = list(self.qcms_attribution.values())
            self.qcms_attribution.clear()
            for i in range(qcms_len):
                self.qcms_attribution[students_emails[i]] = values[i]
            return True
        else:
            return False
    
    def get_statements_len(self) -> int:
        return len(list(self.qcms_attribution.values())[0].statements)
    
    def get_qcms_len(self) -> int:
        return len(self.qcms_attribution)
    
    def get_students_count(self) -> int:
        count = 0
        for keys in self.qcms_attribution:
            if keys.contains("@"):
                count += 1
        return count
    
    def contains_student(self, student_email: str) -> bool:
        for emails in self.qcms_attribution:
            if student_email == emails:
                return True
        return False
    
    def get_registering_line(self) -> list:
        line_to_add = [self.id, self.owner_email]
        statements_str = self.statements[0].id
        stats_str = self.stats[0].id
        for i in range(1, self.get_statements_len()):
            statements_str += ";" + self.statements[i].id
            stats_str += ";" + self.stats[i].id
        line_to_add.append(statements_str)
        line_to_add.append(stats_str)
            
        return line_to_add

    def generate_id(self) -> str:
        self.id = hash(str(uuid4()))
        return self.id