from utilities import *
from user import Student, Teacher
from objects import *
from random import sample, randint, shuffle
from itertools import combinations

class TeachersData():
    def __init__(self) -> None:
        self.save_file = create_save_file("teachers.txt")
        self.users_array = []
        tab = read_file(self.save_file)
        for row in tab:
            if len(row) > 4:
                self.users_array.append(Teacher(email=row[0], password=row[1], name=row[2], firstname=row[3], tags_array=list(map(str, row[4].split(";"))), do_hash=False))
    
    def get_user_by_email(self, email) -> Teacher:
        for users in self.users_array:
            if email == users.email:
                return users
        return None
    
    def contains_user(self, user: Teacher) -> bool:
        return self.get_user_by_email(user.email) != None
    
    def update_user_data(self, user: Teacher) -> None:
        set_lines_which_contains(self.save_file, user.email, user.get_registering_line())

    def add_user(self, user: Teacher) -> bool:
        if not(self.contains_user(user)):
            add_line_to_file(self.save_file, user.get_registering_line())
            self.users_array.append(user)
            return True
        else:
            return False
    
    def add_tag_to_user_by_email(self, email: str, tag:str) -> bool:
        user = self.get_user_by_email(email)
        if user != None and user.add_tag(tag):
            set_lines_which_contains(self.save_file, email, user.get_registering_line())
            return True
        else:
            return False
    
    def remove_tag_to_user_by_email(self, email: str, tag: str) -> bool:
        user = self.get_user_by_email(email)
        if user != None and user.remove_tag(tag):
            set_lines_which_contains(self.save_file, email, user.get_registering_line())
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
    

class StudentsData():
    def __init__(self) -> None:
        self.save_file = create_save_file("students.txt")
        self.users_array = []
        tab = read_file(self.save_file)
        for row in tab:
            if len(row) > 4:
                self.users_array.append(Student(email=row[0], password=row[1], student_number=row[2], name=row[3], firstname=row[4], do_hash=False))
    
    def get_user_by_email(self, email: str) -> Student:
        for users in self.users_array:
            if email == users.email:
                return users
        return None
    
    def get_user_by_student_number(self, student_number: str) -> Student:
        for users in self.users_array:
            if student_number == users.student_number:
                return users
        return None
    
    def contains_user(self, user: Student) -> bool:
        return self.get_user_by_student_number(user.student_number) != None

    def add_user(self, user: Student) -> bool:
        if not(self.contains_user(user)):
            add_line_to_file(self.save_file, user.get_registering_line())
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

    def update_user_data(self, user: Student) -> None:
        set_lines_which_contains(self.save_file, user.email, user.get_registering_line())

    def create_accounts_from_tab(self, tab: list) -> bool:
        new_students = []
        total_success = True
        for lines in tab:
            if len(lines) == 3:
                email = lines[1] + "." + lines[0] + "@etu.umontpellier.fr"
                new_students.append(Student(email=email, password=lines[2], student_number=lines[2], name=lines[0], firstname=lines[1], do_hash=True))
            else:
                total_success = False
        for students in new_students:
            if not(self.contains_user(students)):
                self.add_user(students)
            else:
                total_success = False
        return total_success
    
    def create_accounts_from_csv(self, csv_file_name: str) -> bool:
        return self.create_accounts_from_tab(read_csv(csv_file_name))


class StatementsData():
    def __init__(self) -> None:
        self.save_file = create_save_file("statements.txt")
        self.statements_array = []
        self.random_statements_array = []
        tab = read_file(self.save_file)
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

    def contains_name(self, name: str) -> bool:
        for statement in self.statement_array:
            if statement.name == name:
                return True
        return False

    def contains_statement(self, statement: Statement) -> bool:
        return self.contains_id(statement.id)

    def add_statement(self, statement: Statement) -> bool:
        if not(self.contains_statement(statement)):
            add_line_to_file(self.save_file, statement.get_registering_line())
            self.statements_array.append(statement)
            return True
        else:
            return False
    
    def remove_statement_by_id(self, id: str) -> bool:
        if self.contains_id(id):
            self.statements_array.remove(self.get_statement_by_id(id))
            remove_lines_which_contains(self.save_file, string=id)
            return True
        else:
            return False
    
    def remove_statement(self, statement: Statement) -> bool:
        if self.contains_statement(statement):
            self.statements_array.remove(statement)
            remove_lines_which_contains(self.save_file, string=statement.id)
            return True
        else:
            return False
    
    def get_all_statements(self) -> list:
        return self.statements_array
    
    def statement_is_in_list(self, statement: Statement, array: list) -> bool:
        for elements in array:
            if statement.id == elements.id:
                return True
        return False
    
    def get_all_statements_with_all_tags(self, tags_array: list, teacher_email: str, ignore_statements: list = []) -> list:
        result = []
        statements_from_user = self.get_statements_from_user(teacher_email)
        for statements in sample(statements_from_user, len(statements_from_user)):
            if not(self.statement_is_in_list(statements, ignore_statements)):
                all_tags = True
                for tags in tags_array:
                    if not(tags in statements.tags):
                        all_tags = False
                if all_tags:
                    result.append(statements)
        return result
    
    def get_all_statements_with_any_tag(self, tags_array: list, teacher_email: str, ignore_statements: list = []) -> list:
        result = []
        statements_from_user = self.get_statements_from_user(teacher_email)
        for statements in sample(statements_from_user, len(statements_from_user)):
            if not(self.statement_is_in_list(statements, ignore_statements)):
                for tags in tags_array:
                    if tags in statements.tags:
                        result.append(statements)
                        break
        return result
    
    def get_n_statements_with_tags(self, tags_array: list, n: int, teacher_email: str, ignore_statements: list = []) -> list:
        result = []
        count = 0
        if n <= 0:
            return []
        statements_from_user = self.get_statements_from_user(teacher_email)
        for statements in sample(statements_from_user, len(statements_from_user)):
            if not(self.statement_is_in_list(statements, ignore_statements)):
                all_tags = True
                for tags in tags_array:
                    if not(tags in statements.tags):
                        all_tags = False
                if all_tags:
                    result.append(statements)
                    count += 1
                if count >= n:
                    return result
        return []
    
    def get_random_n_statements_with_tags(self, tags_array: list, n: int, teacher_email: str, ignore_statements: list = []) -> list:
        result = []
        count = 0
        if n <= 0:
            return []
        statements_from_user = self.get_statements_from_user(teacher_email)
        for statements in sample(statements_from_user, len(statements_from_user)):
            if not(self.statement_is_in_list(statements, ignore_statements)):
                all_tags = True
                for tags in tags_array:
                    if not(tags in statements.tags):
                        all_tags = False
                if all_tags:
                    result.append(statements)
                    count += 1
                if count >= n:
                    return result
        return []
    
    def get_statements_with_tags_dic(self, tags_dic: dict, teacher_email: str, Pignore_statements: list = []) -> list:
        statements = []
        ignore_statements = Pignore_statements
        for tags in tags_dic:
            n_statements = self.get_n_statements_with_tags(tags_array=tags, n=tags_dic[tags], teacher_email=teacher_email, ignore_statements=ignore_statements)
            if n_statements != []:
                statements += n_statements
                ignore_statements += n_statements
            else:
                return []
        return statements
    
    def generate_uplets_to_exclude(self, nb_differents_statements: int, qcms_len: int):
        i = 0
        all_combinations = []
        while len(all_combinations) < qcms_len:
            if i > nb_differents_statements:
                return []
            all_combinations += list(combinations(sample(list(range(0, nb_differents_statements)), nb_differents_statements), i))
            i+=1
        return all_combinations[:qcms_len]
        
    
    def get_random_sets_of_qcm(self, tags_dic: dict, teacher_email: str, n: int, randomize: bool = False) -> list:
        qcms = []
        all_statements_with_tags = self.get_all_statements_with_any_tag(list(tags_dic.keys()), teacher_email)
        uplets_to_exclude = self.generate_uplets_to_exclude(len(all_statements_with_tags), n)
        if not uplets_to_exclude:
            return []
        count = 0
        for _ in range(n):
            ignore_statements_indexes = uplets_to_exclude[count]
            ignore_statements = []
            for i in range(len(ignore_statements_indexes)):
                ignore_statements.append(all_statements_with_tags[i])
            statements = []
            for tags in tags_dic:
                for _ in range(tags_dic[tags]):
                    one_statement = self.get_random_n_statements_with_tags(tags_array=[tags], n=1, teacher_email=teacher_email, ignore_statements=ignore_statements)
                    if one_statement != []:
                        statements.append(one_statement[0])
                    else:
                        return []
            if randomize:
                shuffle(statements)
            qcms.append(QCM(name="Questionnaire", statements=statements, user_email=teacher_email))
            count+=1
        return qcms
    
    def get_random_sets_of_qcm_with_range(self, tags_ranges: dict, total_statements: int, teacher_email: str, n: int, randomize: bool = False) -> list:
        min_sum = 0
        max_sum = 0
        for ranges in list(tags_ranges.values()):
            min_sum += ranges[0]
            max_sum += ranges[1]
        if min_sum <= total_statements and total_statements <= max_sum:
            return []
        qcms = []
        all_statements_with_tags = self.get_all_statements_with_any_tag(list(tags_ranges.keys()), teacher_email)
        uplets_to_exclude = self.generate_uplets_to_exclude(len(all_statements_with_tags), n)
        if not uplets_to_exclude:
            return []
        count = 0
        for _ in range(n):
            ignore_statements_indexes = uplets_to_exclude[count]
            ignore_statements = []
            for i in range(len(ignore_statements_indexes)):
                ignore_statements.append(all_statements_with_tags[i])
            statements = []
            one_student_ranges = {}
            total_sum = 0
            while total_sum != total_statements:
                total_sum = 0
                for tags in tags_ranges:
                    random_nb = randint(tags_ranges[tags][0], tags_ranges[tags][1])
                    one_student_ranges[tags] = random_nb
                    total_sum += random_nb
            for tags in one_student_ranges:
                for _ in range(one_student_ranges[tags]):
                    one_statement = self.get_random_n_statements_with_tags(tags_array=[tags], n=1, teacher_email=teacher_email, ignore_statements=ignore_statements)
                    if one_statement != []:
                        statements.append(one_statement[0])
                    else:
                        return []
            if randomize:
                shuffle(statements)
            qcms.append(QCM(name="Questionnaire", statements=statements, user_email=teacher_email))
            count+=1
        return qcms
    
    def get_statement_by_id(self, id: str) -> Statement:
        for statements in self.statements_array:
            if statements.id == id:
                return statements
        return None
    
    def get_statements_from_user(self, email) -> list:
        result = []
        for statements in self.statements_array:
            if statements.user_email == email:
                result.append(statements)
        return result
    
    def set_statement(self, id: str, new_statement: Statement) -> None:
        statement = self.get_statement_by_id(id)
        statement.set(new_statement=new_statement)
        set_lines_which_contains(self.save_file, id, statement.get_registering_line())
    
    def get_statements_with_any_tag(self, tags) -> list:
        statements_with_tag = []
        for statement in self.statements_array:
            for tag in tags:
                if statement not in statements_with_tag and tag in statement.tags:
                    statements_with_tag.append(statement)
        return statements_with_tag
    
    def get_statements_with_all_tag(self, tags) -> list:
        statements_with_tag = []
        for statement in self.statements_array:
            all_tags = True
            for tag in tags:
                if tag not in statement.tags:
                    all_tags = False
            if all_tags:
                statements_with_tag.append(statement)
        return statements_with_tag

class QCMData():
    def __init__(self, statements_data: StatementsData) -> None:
        self.save_file = create_save_file("qcm.txt")
        self.statements_data = statements_data
        self.qcm_array = []
        tab = read_file(self.save_file)
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

    def add_qcm(self, qcm: QCM) -> bool:
        if not(self.contains_qcm(qcm)):
            add_line_to_file(self.save_file, qcm.get_registering_line())
            self.qcm_array.append(qcm)
            return True
        else:
            return False
    
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

    def remove_qcm_by_id(self, id: str) -> bool:
        if self.contains_id(id):
            self.qcm_array.remove(self.get_qcm_by_id(id))
            remove_lines_which_contains(self.save_file, string=id)
            return True
        else:
            return False
    
    def remove_qcm(self, qcm: QCM) -> bool:
        if self.contains_qcm(qcm):
            self.qcm_array.remove(qcm)
            remove_lines_which_contains(self.save_file, string=qcm.id)
            return True
        else:
            return False

class LiveStatementsStatsData():
    def __init__(self) -> None:
        self.save_file = create_save_file("livestatementsstats.txt")
        self.livestatementsstats_array = []
        tab = read_file(self.save_file)
        for row in tab:
            if len(row) > 5 :
                stats = {}
                all_students_data = row[3].split(";")
                for each_students_data in all_students_data:
                    dic_infos = each_students_data.split(":")
                    try: 
                        stats[dic_infos[0]] = {"responses": list(map(int, dic_infos[1].split(","))), "time": float(dic_infos[2]), "validity" : str(dic_infos[3])}
                    except ValueError:
                        stats[dic_infos[0]] = {"responses": list(map(str, dic_infos[1].split(","))), "time": float(dic_infos[2]), "validity" : str(dic_infos[3])}
                joins_leaves = []
                joins_leaves_str = row[4].split(";")
                for pairs_str in joins_leaves_str:
                    pairs = pairs_str.split(":")
                    joins_leaves.append((pairs[0], pairs[1]))
                self.livestatementsstats_array.append(LiveStatementStats(id=row[0], start_time=float(row[1]), end_time=float(row[2]), stats=stats, joins_leaves=joins_leaves))

    def contains_id(self, id: str):
        for livestatementsstats in self.livestatementsstats_array:
            if livestatementsstats.id == id:
                return True
        return False
    
    def contains_livestatementsstats(self, livestatementsstats: LiveStatementStats) -> bool:
        return self.contains_id(livestatementsstats.id)

    def add_livestatementsstats(self, livestatementsstats: LiveStatementStats) -> bool:
        if not(self.contains_livestatementsstats(livestatementsstats)):
            self.livestatementsstats_array.append(livestatementsstats)
            return True
        else:
            return False
    
    def save_livestatementsstats_to_file(self, livestatementsstats: LiveStatementStats) -> None:
        add_line_to_file(self.save_file, livestatementsstats.get_registering_line())
    
    def get_all_livestatementsstats(self) -> list:
        return self.livestatementsstats_array
    
    def get_livestatementsstats_by_id(self, id: str) -> LiveQCM:
        for livestatementsstats in self.livestatementsstats_array:
            if livestatementsstats.id == id:
                return livestatementsstats
        return None
    
    def get_livestatementsstats_by_student_email(self, student_email: str) -> LiveQCM:
        for livestatementsstats in self.livestatementsstats_array:
            if livestatementsstats.contains_student(student_email):
                return livestatementsstats
        return None

    def remove_livestatementsstats_by_id(self, id: str) -> bool:
        if self.contains_id(id):
            self.livestatementsstats_array.remove(self.get_livestatementsstats_by_id(id))
            remove_lines_which_contains(self.save_file, string=id)
            return True
        else:
            return False
    
    def remove_livestatementsstats(self, liveqcm: LiveStatementStats) -> bool:
        if self.contains_livestatementsstats(liveqcm):
            self.livestatementsstats_array.remove(livestatementsstats_data)
            remove_lines_which_contains(self.save_file, string=liveqcm.id)
            return True
        else:
            return False

class LiveQCMData():
    def __init__(self, statements_data: StatementsData, livestatementsstats_data: LiveStatementsStatsData) -> None:
        self.save_file = create_save_file("liveqcm.txt")
        self.statements_data = statements_data
        self.livestatementsstats_data = livestatementsstats_data
        self.liveqcm_array = []
        tab = read_file(self.save_file)
        for row in tab:
            if len(row) > 3:
                statements_ids = row[2].split(";")
                livestatementsstats_ids = row[3].split(";")
                statements = []
                is_anything_none = False
                for ids in statements_ids:
                    statement = self.statements_data.get_statement_by_id(ids)
                    if statement is not None:
                        statements.append(statement)
                    else:
                        is_anything_none = True
                stats = []
                for ids in livestatementsstats_ids:
                    stat = self.livestatementsstats_data.get_livestatementsstats_by_id(ids)
                    if stat is not None:
                        stats.append(stat)
                    else:
                        is_anything_none = True
                if not(is_anything_none):
                    self.liveqcm_array.append(LiveQCM(id=row[0], owner_email=row[1], statements=statements, stats=stats, opened=False))
                else:
                    self.remove_liveqcm_by_id(row[0])

    def contains_id(self, id: str):
        for liveqcm in self.liveqcm_array:
            if liveqcm.id == id:
                return True
        return False
    
    def contains_liveqcm(self, liveqcm: LiveQCM) -> bool:
        return self.contains_id(liveqcm.id)

    def add_liveqcm(self, liveqcm: LiveQCM) -> bool:
        if not(self.contains_liveqcm(liveqcm)):
            self.liveqcm_array.append(liveqcm)
            return True
        else:
            return False
    
    def save_liveqcm_to_file(self, liveqcm: LiveQCM) -> None:
        add_line_to_file(self.save_file, liveqcm.get_registering_line())
        for stats in liveqcm.stats:
            livestatementsstats_data.save_livestatementsstats_to_file(stats)

    def end_and_save_liveqcm(self, liveqcm: LiveQCM) -> None:
        liveqcm.end()
        self.save_liveqcm_to_file(liveqcm)
    
    def end_and_save_liveqcm_by_id(self, id: str) -> bool:
        if self.contains_id(id):
            self.end_and_save_liveqcm(self.get_liveqcm_by_id(id))
            return True
        else:
            return False
    
    def get_all_liveqcm(self) -> list:
        return self.liveqcm_array
    
    def get_opened_liveqcm(self) -> list:
        opened_liveqcm = []
        for liveqcm in self.liveqcm_array:
            if liveqcm.opened:
                opened_liveqcm.append(liveqcm)
        return opened_liveqcm
    
    def get_closed_liveqcm(self) -> list:
        closed_liveqcm = []
        for liveqcm in self.liveqcm_array:
            if not(liveqcm.opened):
                closed_liveqcm.append(liveqcm)
        return closed_liveqcm
    
    def get_liveqcm_from_user(self, email: str) -> list:
        result = []
        for liveqcm in self.liveqcm_array:
            if liveqcm.owner_email == email:
                result.append(liveqcm)
        return result
    
    def get_liveqcm_by_id(self, id: str) -> LiveQCM:
        for liveqcm in self.liveqcm_array:
            if liveqcm.id == id:
                return liveqcm
        return None
    
    def get_all_closed_liveqcm_from_owner(self, owner_email: str) -> list:
        liveqcm_array = []
        for liveqcm in self.liveqcm_array:
            if liveqcm.owner_email == owner_email and not(liveqcm.opened):
                liveqcm_array.append(liveqcm)
        return liveqcm_array
    
    def get_opened_liveqcm_by_owner_email(self, email: str) -> LiveQCM:
        for liveqcm in self.liveqcm_array:
            if liveqcm.owner_email == email and liveqcm.opened:
                return liveqcm
        return None
    
    def get_liveqcm_by_student_email(self, student_email: str) -> LiveQCM:
        for liveqcm in self.get_opened_liveqcm():
            if liveqcm.contains_student(student_email):
                return liveqcm
        return None

    def remove_liveqcm_by_id(self, id: str) -> bool:
        remove_lines_which_contains(self.save_file, string=id)
        if self.contains_id(id):
            self.liveqcm_array.remove(self.get_liveqcm_by_id(id))
            return True
        else:
            return False
        
    
    def remove_liveqcm(self, liveqcm: LiveQCM) -> bool:
        remove_lines_which_contains(self.save_file, string=liveqcm.id)
        if self.contains_liveqcm(liveqcm):
            self.liveqcm_array.remove(liveqcm)
            return True
        else:
            return False

class TestsData():
    def __init__(self) -> None:
        self.save_file = create_save_file("tests.txt")
        self.tests_array = []
        tab = read_file(self.save_file)
        for row in tab:
            if len(row) > 3:
                statements_ids = row[2].split(";")
                livestatementsstats_ids = row[3].split(";")
                statements = []
                is_anything_none = False
                for ids in statements_ids:
                    statement = self.statements_data.get_statement_by_id(ids)
                    if statement is not None:
                        statements.append(statement)
                    else:
                        is_anything_none = True
                stats = []
                for ids in livestatementsstats_ids:
                    stat = self.livestatementsstats_data.get_livestatementsstats_by_id(ids)
                    if stat is not None:
                        stats.append(stat)
                    else:
                        is_anything_none = True
                if not(is_anything_none):
                    self.liveqcm_array.append(LiveQCM(id=row[0], owner_email=row[1], statements=statements, stats=stats, opened=False))
                else:
                    self.remove_liveqcm_by_id(row[0])

    def contains_id(self, id: str):
        for liveqcm in self.liveqcm_array:
            if liveqcm.id == id:
                return True
        return False
    
    def contains_liveqcm(self, liveqcm: LiveQCM) -> bool:
        return self.contains_id(liveqcm.id)

    def add_liveqcm(self, liveqcm: LiveQCM) -> bool:
        if not(self.contains_liveqcm(liveqcm)):
            self.liveqcm_array.append(liveqcm)
            return True
        else:
            return False
    
    def save_liveqcm_to_file(self, liveqcm: LiveQCM) -> None:
        add_line_to_file(self.save_file, liveqcm.get_registering_line())
        for stats in liveqcm.stats:
            livestatementsstats_data.save_livestatementsstats_to_file(stats)

    def end_and_save_liveqcm(self, liveqcm: LiveQCM) -> None:
        liveqcm.end()
        self.save_liveqcm_to_file(liveqcm)
    
    def end_and_save_liveqcm_by_id(self, id: str) -> bool:
        if self.contains_id(id):
            self.end_and_save_liveqcm(self.get_liveqcm_by_id(id))
            return True
        else:
            return False
    
    def get_all_liveqcm(self) -> list:
        return self.liveqcm_array
    
    def get_opened_liveqcm(self) -> list:
        opened_liveqcm = []
        for liveqcm in self.liveqcm_array:
            if liveqcm.opened:
                opened_liveqcm.append(liveqcm)
        return opened_liveqcm
    
    def get_closed_liveqcm(self) -> list:
        closed_liveqcm = []
        for liveqcm in self.liveqcm_array:
            if not(liveqcm.opened):
                closed_liveqcm.append(liveqcm)
        return closed_liveqcm
    
    def get_liveqcm_from_user(self, email: str) -> list:
        result = []
        for liveqcm in self.liveqcm_array:
            if liveqcm.owner_email == email:
                result.append(liveqcm)
        return result
    
    def get_liveqcm_by_id(self, id: str) -> LiveQCM:
        for liveqcm in self.liveqcm_array:
            if liveqcm.id == id:
                return liveqcm
        return None
    
    def get_all_closed_liveqcm_from_owner(self, owner_email: str) -> list:
        liveqcm_array = []
        for liveqcm in self.liveqcm_array:
            if liveqcm.owner_email == owner_email and not(liveqcm.opened):
                liveqcm_array.append(liveqcm)
        return liveqcm_array
    
    def get_opened_liveqcm_by_owner_email(self, email: str) -> LiveQCM:
        for liveqcm in self.liveqcm_array:
            if liveqcm.owner_email == email and liveqcm.opened:
                return liveqcm
        return None
    
    def get_liveqcm_by_student_email(self, student_email: str) -> LiveQCM:
        for liveqcm in self.get_opened_liveqcm():
            if liveqcm.contains_student(student_email):
                return liveqcm
        return None

    def remove_liveqcm_by_id(self, id: str) -> bool:
        remove_lines_which_contains(self.save_file, string=id)
        if self.contains_id(id):
            self.liveqcm_array.remove(self.get_liveqcm_by_id(id))
            return True
        else:
            return False
        
    
    def remove_liveqcm(self, liveqcm: LiveQCM) -> bool:
        remove_lines_which_contains(self.save_file, string=liveqcm.id)
        if self.contains_liveqcm(liveqcm):
            self.liveqcm_array.remove(liveqcm)
            return True
        else:
            return False

def init():
    global teachers_data
    teachers_data = TeachersData()
    global students_data
    students_data = StudentsData()
    global statements_data
    statements_data = StatementsData()
    global qcm_data
    qcm_data = QCMData(statements_data=statements_data)
    global livestatementsstats_data
    livestatementsstats_data = LiveStatementsStatsData()
    global liveqcm_data
    liveqcm_data = LiveQCMData(statements_data=statements_data, livestatementsstats_data=livestatementsstats_data)