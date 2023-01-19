from hashlib import md5
from time import time

def hash(word: str) -> str:
    return md5(word.encode("utf-8")).hexdigest()


password = "eee"
password_hash = hash(password)
print("Mot de passe : " + password + "\nHash : " + password_hash + "\n")

start_time = time()
for i in range(7):
    for j in range(26):