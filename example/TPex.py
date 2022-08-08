# TP Exemple (avec erreur)

# Exercice 1
# Question 1 : calcul de la moyenne d'une liste


def moyenne(L):
    s = 0
    for e in L:
        s += e
    return s/len(L)

# Question 2 : calcul de la variance d'une liste


def variance(L):
    s1 = L[0]
    s2 = L[0]
    for i in range(1, len(L)):
        s1 += L[i]
        s2 += L[i]**2
    return s2//len(L)-(s1//len(L))**2


# Exercice 2
# Question 1 : détermine si tous les éléments d'une liste sont positifs


def tout_positif(L):
    i = 0
    while L[i] >= 0:
        pass
    if i == len(L):
        return True
    else:
        return False

# Question 2 : détermine si tous les éléments d'une liste supérieur à b


def tout_superieur(L, b):
    for e in L:
        if e < b:
            print(e)
            return False
    return True


# Question 3 : déterminer si au moins un élément d'une liste est positif


def existe_positif(L):
    for e in L:
        if e > 0:
            return True
    return False

# Exercice 3
# Question 1 : convertit en seconde une durée donnée par une liste
#              [jour, heures, minutes, secondes]


def duree_secondes(L):
    return 24*60*60*L[1]+60*60*L[2]+60*L[3]+L[4]


# Exercice 4
# Question 1 : en utilisant la fonction choice du module random :
#              "from random import choice"
#              génère aléatoirement une chaîne de caractères de longueur n
#              constituée uniquement des caractères A, C, T, G.


from random import choice


def generation(n):
    s = ""
    for i in range(n):
        s += choice("ACTG")
    return s
