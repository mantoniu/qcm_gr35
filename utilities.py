import csv
from hashlib import md5
from os import mkdir, path, stat

global line_separator
line_separator = "@__|||1S"
global row_separator
row_separator = "@__|||2S"

def hash(word: str) -> str:
    word = "Kilian" + word
    result = md5(word.encode("utf-8")).hexdigest()
    return result.replace(";", "P")

def check_hash(word: str, hash: str) -> bool :
    return hash(word) == hash

def add_line_to_file(file_name: str, line: list) -> None:
    with open(file_name,'a') as file:
        if stat(file_name).st_size > 0:
            to_write = line_separator + line[0]
        else:
            to_write = line[0]
        for i in range(1, len(line)):
            to_write += row_separator + line[i]
        file.write(to_write)

def remove_line_to_file(file_name: str, line_to_remove: int) -> None:
    with open(file_name,'r') as file:
        entire_file = file.read()
    with open(file_name, 'w') as file:
        lines = entire_file.split(line_separator)
        for i in range(len(lines)):
            if i != line_to_remove:
                add_line_to_file(file_name=file_name, line=lines[i].split(row_separator))

def remove_lines_to_file(file_name: str, lines_to_remove: list) -> None:
    with open(file_name,'r') as file:
        entire_file = file.read()
    with open(file_name, 'w') as file:
        lines = entire_file.split(line_separator)
        for i in range(len(lines)):
            if not(i in lines_to_remove):
                add_line_to_file(file_name=file_name, line=lines[i].split(row_separator))

def remove_lines_which_contains(file_name: str, string: str) -> None:
    lines_to_remove = []
    with open(file_name,'r') as file:
        entire_file = file.read()
    with open(file_name, 'w') as file:
        lines = entire_file.split(line_separator)
        for i in range(len(lines)):
            rows = lines[i].split(row_separator)
            for row in rows:
                if row == string:
                    lines_to_remove.append(i)
    remove_lines_to_file(file_name=file_name, lines_to_remove=lines_to_remove)

def set_lines_to_file(file_name: str, indexes: int, line: list) -> None:
    with open(file_name,'r') as file:
        entire_file = file.read()
    with open(file_name, 'w') as file:
        lines = entire_file.split(line_separator)
        for i in range(len(lines)):
            if i in indexes:
                add_line_to_file(file_name=file_name, line=line)
            else:
                add_line_to_file(file_name=file_name, line=lines[i])

def set_lines_which_contains(file_name: str, string: str, line: list) -> None:
    lines_to_set = []
    with open(file_name,'r') as file:
        entire_file = file.read()
    lines = entire_file.split(line_separator)
    for i in range(len(lines)):
        rows = lines[i].split(row_separator)
        for row in rows:
            if row == string:
                lines_to_set.append(i)
    set_lines_to_file(file_name=file_name, indexes=lines_to_set, line=line)

def read_file(file_name: str) -> list:
    tab = []
    with open(file_name,'r') as file:
        entire_file = file.read()
        lines = entire_file.split(line_separator)
        for line in lines:
            tab.append(line.split(row_separator))
    return tab

def create_save_file(file_name: str) -> str:
    if not(path.exists("saves")):
        mkdir("saves")
    try:
        f = open("saves/" + file_name, 'x')
        f.close()
    except:
        pass
    return "saves/" + file_name