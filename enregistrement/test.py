from Myobject import MyObject
import pickle

A = MyObject()
B = MyObject()

tab = [A,B]

for i in range(0,len(tab)):
    username = "user"+str(i)
    with open('save','wb') as username:
        pickle.dump(tab[i],f1)

tabres = []

for i in range(0,len(tab)):
    username = "user"+str(i)
    with open('save','wb') as username:
        tabres.append(user+i)
