import csv
from hashlib import md5

global line_separator
line_separator = "@__//1*"
global row_separator
row_separator = "@__//2*"

def hash(word: str) -> str:
    return md5(word.encode("utf-8")).hexdigest()

def check_hash(word: str, hash: str) -> bool :
    return hash(word) == hash

def add_line_to_file(file_name: str, line: list) -> None:
    with open(file_name,'a') as file:
        to_write = line_separator + line[0]
        for i in range(1, len(line)):
            to_write += row_separator + line[i]
        file.write(to_write)

def read_file(file_name: str) -> list:
    tab = []
    with open(file_name,'r') as file:
        entire_file = file.read()
        lines = entire_file.split(line_separator)
        for line in lines:
            tab.append(line.split(row_separator))
    return tab