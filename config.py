#####################################################
#            EXEMPLE DE CONFIGURATION               #
#####################################################

import model as m
import controller as c

session_name = "TP pour l'exemple"

list_questions = []

# Exercice 1 Question 1 Barème 3 pts
# Calculer la moyenne d'une liste

question = {"func_name": "moyenne",
            "number": 1,
            "exercice": 1,
            "scale": 3,
            "test": []}

list_tests = []
list_tests.append({"command": "moyenne([1])",
                   "result": 1,
                   "max_time": 1,
                   "point": 1,
                   "hidden": 0,
                   "custom_var": {}})

list_tests.append({"command": "moyenne([k for k in range(101)])",
                   "result": 50,
                   "max_time": 1,
                   "point": 2,
                   "hidden": 0,
                   "custom_var": {}})

list_tests.append({"command": "moyenne([-k for k in range(20)])",
                   "result": -9.5,
                   "max_time": 1,
                   "point": 2,
                   "hidden": 1,
                   "custom_var": {}})
list_tests.append({"command": ("abs(moyenne([1.2,-1.2,2.4,5.7,-5.7,-2.4]))"
                               "< 10**(-10)"),
                   "result": 1,
                   "max_time": 1,
                   "point": 2,
                   "hidden": 2,
                   "custom_var": {}})

question["test"] = list_tests.copy()

list_questions.append(question.copy())


# Exercice 1 Question 2 Barème 2 pts
# Calculer la varaince d'une liste


question = {"func_name": "variance",
            "number": 2,
            "exercice": 1,
            "scale": 2,
            "test": []}

list_tests = []
list_tests.append({"command": "variance([1])",
                   "result": 0})
list_tests.append({"command": "variance([k for k in range(101)])",
                   "result": 850.0})
list_tests.append({"command": "variance([-k for k in range(20)])",
                   "result": 33.25})
list_tests.append({"command": ("abs(variance([1.2,-1.2,2.4,5.7,-5.7,-2.4])"
                               "-13.23) < 10**(-10)"),
                   "result": True})

question["test"] = list_tests.copy()

list_questions.append(question.copy())


# Exercice 2 Question 1 Barème 2 pts
# Déterminer si tous les éléments d'une liste sont positifs


question = {"func_name": "tout_positif",
            "number": 1,
            "exercice": 2,
            "scale": 2,
            "test": []}

list_tests = []
list_tests.append({"command": "tout_positif([1]*10)",
                   "result": True})
list_tests.append({"command": "tout_positif([0])",
                   "result": True})
list_tests.append({"command": "tout_positif([k for k in range(10)])",
                   "result": True})
list_tests.append({"command": "tout_positif([-1,1,2,3])",
                   "result": False})
list_tests.append({"command": "tout_positif([1,1,2,3,-0.1])",
                   "result": False})
list_tests.append({"command": "tout_positif([1]*5 + [-10.10] + [2]*5)",
                   "result": False})
list_tests.append({"command": "tout_positif([-k for k in range(10)])",
                   "result": False})

question["test"] = list_tests.copy()

list_questions.append(question.copy())


# Exercice 2 Question 2 Barème 2 pts
# Déterminer si au moins un élément d'une liste est positif


question = {"func_name": "existe_positif",
            "number": 2,
            "exercice": 2,
            "scale": 2,
            "test": []}

list_tests = []
list_tests.append({"command": "existe_positif([-1]*10)",
                   "result": False})
list_tests.append({"command": "existe_positif([0])",
                   "result": True})
list_tests.append({"command": "existe_positif([k for k in range(10)])",
                   "result": True})
list_tests.append({"command": "existe_positif([-1,-1,-2,3])",
                   "result": True})
list_tests.append({"command": "existe_positif([1,-1,-2,-3,-0.1])",
                   "result": True})
list_tests.append({"command": "existe_positif([-1]*5 + [10.10] + [-2]*5)",
                   "result": True})
list_tests.append({"command": "existe_positif([-k-1 for k in range(10)])",
                   "result": False})

question["test"] = list_tests.copy()

list_questions.append(question.copy())


# Exercice 3 Question 1 Barème 2 pts
# Convertir en seconde une durée donnée par une liste
# [jour, heures, minutes, secondes]


question = {"func_name": "duree_secondes",
            "number": 1,
            "exercice": 3,
            "scale": 2,
            "test": []}

list_tests = []
list_tests.append({"command": "duree_secondes([0,0,0,30])",
                   "result": 30})
list_tests.append({"command": "duree_secondes([0,0,0,0])",
                   "result": 0})
list_tests.append({"command": "duree_secondes([1,0,0,0])",
                   "result": 86400})
list_tests.append({"command": "duree_secondes([1,1,1,1])",
                   "result": 90061})
list_tests.append({"command": "duree_secondes([0,0,-1,60])",
                   "result": 0})
list_tests.append({"command": "duree_secondes([0,2,0,0])",
                   "result": 7200})

question["test"] = list_tests.copy()

list_questions.append(question.copy())


#####################################################
#         GENERATION DE L'OBJET SESSION             #
#####################################################


session = m.Session(session_name)

for q in list_questions:
    session.add_question(q["func_name"], q["number"],
                         q["exercice"], scale=q["scale"])
    for t in q["test"]:
        if "result" not in t:
            t["result"] = 1
        if "max_time" not in t:
            t["max_time"] = 1
        if "point" not in t:
            t["point"] = 1
        if "level" not in t:
            t["level"] = "error"
        if "hidden" not in t:
            t["hidden"] = 0
        if "custom_var" not in t:
            t["custom_var"] = {}

        session.add_test(t["command"], t["result"], t["max_time"], t["point"],
                         t["level"], t["hidden"], t["custom_var"])

work = c.Work(session)
