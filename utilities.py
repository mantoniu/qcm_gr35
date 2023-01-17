import csv
from hashlib import md5

def hash(word: str) -> str:
    return md5(word.encode("utf-8")).hexdigest()

def check_hash(word: str, hash: str) -> bool :
    return hash(word) == hash

def add_line_to_csv(csv_file: str, line: list) -> None:
    with open(csv_file,'a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(line)
    file.close()

def read_csv(csv_file: str) -> list(list(str)):
    tab = []
    with open(csv_file,'r') as file:
        reader = csv.reader(file)
        for row in reader:
            tab.append(row)
    file.close()
    return tab