import csv
import hashlib

users_list = []

def checkPassword(password: str,hash: str):
    return hashlib.md5(password.encode("utf-8")).hexdigest() == hash

def containsUser(user: str):
    for elem in users_list:
        if(user==elem[0]):
            return True
    return False

def addUser(name: str,password: str):
    addLine('saves/users.csv',[name,hashlib.md5(password.encode("utf-8")).hexdigest()])

def addLine(csv_file: str, line: list): 
    if(not(containsUser(line[0]))):
        with open(csv_file,'a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(line)
        file.close()

def readCsv(csv_file: str):
    with open(csv_file,'r') as file:
        reader = csv.reader(file)
        for row in reader:
            users_list.append(row)
    file.close()


readCsv("saves/users.csv")
print(users_list)
print(checkPassword("azerty",users_list[1][1]))