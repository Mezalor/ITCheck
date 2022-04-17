class Session:
    """
    Sujet du TP contenant les questions et tests à effectuer
    """
    def __init__(self, name, module=[]):
        """
        name : nom du sujet de TP
        module : liste des noms des modules à importer pour les tests
        """
        self.name = name
        self.module = module
        # Liste des questions
        self.list_questions = []

    def add_question(self, func_name, number=-1,
                     exercice="", name="", scale=-1):
        """ Ajoute une question
        func_name : nom de la fonction ou variable demandé en réponse
                    de la question
        number : numéro de la question
                 si -1 vaut le nombre de questions dans list_questions plus 1
        exercice : numéro ou nom de l'exercice
                   si "" alors pas de nom d'exercice affiché
        name : nom de la question
               si différent de "" alors est affiché à la place de number
        scale : nombre de points de la question
                Si -1 alors le barème de la question est égal à la somme des
                points des tests associés à la question
        """
        if number == -1:
            number = len(self.list_questions)
        q = Question(number, func_name, exercice, name, scale)
        self.list_questions.append(q)

    def add_test(self, command, result, max_time=1, point=1,
                 level="critic", hidden=0, custom_var={}, question_id=-1):
        """
        command : nom de l'instruction à executer pour le test
        result : le résultat attendu. Cela peut être une instruction
        max_time : temps maximal d'execution du test en seconde
        point : nombre de point que rapporte le test en cas de succès
        level : le niveau de criticité du test (fatal, critic, error, warning)
            fatal : on arrête les tests et on met 0 à la question
            critic : le test ne rapporte aucun point et on continue les tests
                     En cas d'erreur d'execution on met 0 à la question
                     et on arrète les tests
            error : le test ne rapporte aucun point et on continue les tests
            warning : le test n'enlève pas de point en cas d'échec
        hidden : détermine si le test doit être caché
            0 : le test et le résultat attendu sont affichés
            1 : seul le résultat attendu est affiché
            2 : seul le résultat obtenu est affiché (utile pour les variables)
        custom_var : disctionnaire contenant des variables personalisées
                     (par ex des fonctions) pour effectuer le test.
                     La clef est le nomn de la variable et la valeur sa def
        question_id : numéro de la question a laquelle le test est associé
                      si -1 alors le test est ajouté à la dernière question
        """
        if question_id != -1:
            i = question_id
        else:
            i = self.get_number_questions()-1
        self.list_questions[i].add_test(command, result, max_time,
                                        point, level, hidden, custom_var)

    def get_total_scale(self):
        """ Total de points du sujet """
        return sum([q.get_scale() for q in self.list_questions])

    def get_number_questions(self):
        """ Nombre total de questions """
        return len(self.list_questions)

    def get_number_tests(self):
        """ Nombre total de tests """
        return sum([q.get_number_tests() for q in self.list_questions])

    def get_question_byid(self, id):
        """ Renvoie la question numéro id """
        return self.list_questions[id]


class Question:
    """
    Question d'un sujet contenant les test à réaliser
    """
    def __init__(self, number, func_name, exercice="", name="", scale=-1):
        """
        number : numéro de la question
        func_name : nom de la fonction ou variable demandé en réponse
                    de la question
        exercice : numéro ou nom de l'exercice
                   si vaut "" alors pas de nom d'exercice affiché
        name : nom de la question qui sera affiché
               si vaut "" alors seul le numéro de question/exercice est affiché
        scale : nombre de points de la question
                Si -1 alors le barème de la question est égal à la somme des
                points des tests associés à la question
        """
        self.number = str(number)
        self.func_name = func_name
        self.exercice = str(exercice)
        self.name = name
        self.scale = scale
        # Liste des tests de la question
        self.list_tests = []

    def add_test(self, command, result, max_time=1, point=1,
                 level="critic", hidden=0, custom_var={}):
        """
        command : nom de l'instruction à executer pour le test
        result : le résultat attendu
        max_time : temps maximal d'execution du test en seconde
        point : nombre de point que rapporte le test en cas de succès
        level : le niveau de criticité du test (fatal, critic, error, warning)
            fatal : on arrête les tests et on met 0 à la question
            critic : le test ne rapporte aucun point et on continue les tests
                     En cas d'erreur d'execution on met 0 à la question
                     et on arrète les tests
            error : le test ne rapporte aucun point et on continue les tests
            warning : le test n'enlève pas de point en cas d'échec
        hidden : détermine si le test doit être caché
            0 : le test et le résultat attendu sont affichés
            1 : seul le résultat attendu est affiché
            2 : seul le résultat obtenu est affiché (utile pour les variables)
        custom_var : disctionnaire contenant des variables personalisées
                     (par ex des fonctions) pour effectuer le test.
                     La clef est le nomn de la variable et la valeur sa def
        """
        t = Test(self.func_name, command, result, max_time, point,
                 level, hidden, custom_var)
        self.list_tests.append(t)

    def get_total_points_test(self):
        return sum([t.get_point() for t in self.list_tests])

    def get_scale(self):
        if self.scale != -1:
            return self.scale
        else:
            return self.get_total_points_test()

    def get_number_tests(self):
        """ Nombre total de test à la question """
        return len(self.list_tests)

    def get_name(self):
        if self.name != "":
            return self.name
        elif self.exercice != "":
            return "Exercice " + self.exercice + " | Question " + self.number
        else:
            return "Question " + self.number

    def get_func_name(self):
        return self.func_name

    def get_test_byid(self, id):
        return self.list_tests[id]


class Test:
    """
    Test sur une fonction définie par une question
    """
    def __init__(self, func_name, command, result, max_time,
                 point, level, hidden, custom_var):
        """
        func_name : nom de la fonction ou variable testée
        command : nom de l'instruction à executer pour le test
        result : le résultat attendu (peut être une instruction)
        max_time : temps maximal d'execution du test en seconde
        point : nombre de point que rapporte le test en cas de succès
        level : le niveau de criticité du test (fatal, critic, error, warning)
            fatal : on arrête les tests et on met 0 à la question
            critic : le test ne rapporte aucun point et on continue les tests
                     En cas d'erreur d'execution on met 0 à la question
                     et on arrète les tests
            error : le test ne rapporte aucun point et on continue les tests
            warning : le test n'enlève pas de point en cas d'échec
        hidden : détermine si le test doit être caché
            0 : le test et le résultat attendu sont affichés
            1 : seul le résultat attendu est affiché
            2 : seul le résultat obtenu est affiché (utile pour les variables)
        custom_var : disctionnaire contenant des variables personalisées
                     (par ex des fonctions) pour effectuer le test.
                     La clef est le nomn de la variable et la valeur sa def
        """
        self.func_name = func_name
        self.command = command
        self.result = result
        self.max_time = max_time
        self.point = point
        self.level = level
        self.hidden = hidden
        self.custom_var = custom_var

    def show_command(self):
        return self.command

    def get_command(self):
        func_name = "work_module." + self.func_name
        res = self.command.replace(self.func_name, func_name)
        for var in self.custom_var:
            var2 = "work_module." + var
            res = res.replace(var, var2)
        return res

    def get_result(self):
        return self.result

    def get_max_time(self):
        return self.max_time

    def get_point(self):
        return self.point

    def get_level(self):
        return self.level

    def get_hidden(self):
        return self.hidden

    def get_custom_var(self):
        return self.custom_var
