import time as t

POURCENT = 0.35
T_MAX = 30#s    en seconde

liste = []

for j in range (100):
    var = input("donne un nom d'utilisatur")  #simule l'envoie d'un msg par un utilisateur
    liste.append((var,t.time())) # sauvegarde de l'envoie d'un msg d'un utilisateur

    for i in range (len(liste)-1,-1,-1): # supprime tout les msg plus vieux que 30 s
        if liste[i][1] < t.time()-T_MAX :      # 30 s est prix arbitrairement
            liste.pop(i)

     # compte le nombre de msg envoyer par chaque personne
    Data = dict()
    for i in liste:
        try:
            Data[i[0]] = Data[i[0]] + 1
        except KeyError:
            Data[i[0]] = 1
    msgVar = Data[var]

    if (msgVar/len(liste) < POURCENT) or len(liste)<4: # gagne des pts si il y a pas eu de msg depuis
        print("Point gagner")                           # longtemps ou si on reprsent - d'un certain
        #donner pts d'xp                                # pourcentage des msg envoyer

    print(msgVar)
    print(msgVar/len(liste))

    Data = dict()
    for i in liste:
        try:
            Data[i[0]] = Data[i[0]] + 1
        except KeyError:
            Data[i[0]] = 1


    print(Data)


def xpVersLevel(nombre):
    return (2*nombre + 1) # fonction qui donner le niveau en fonction de pts d'xp

def levelVersXp(nombre):
    return (nombre/2 -1) # donne le nombre de pts d'xp en fonction du level




