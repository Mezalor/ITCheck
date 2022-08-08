import timeout_unix as to
# import timeout_windows as to
from io import StringIO
import sys


class Work:

    def __init__(self, session, file_loc="", max_time_import=2):
        """
        session : Objet de type model.Session contenant le sujet du TP :
                  ie les questions et tests à réaliser
        file_loc : chemin du fichier réponse (fichier python où se
                                               trouve les fonctions à tester)
        max_time_import : temps maximal en sec pour l'importation du fichier
        """
        self.session = session
        self.file_loc = file_loc
        self.max_time_import = max_time_import
        # Le module contenant les fonctions du travail évalué
        self.work_module = None
        # Liste à deux entrées [question_id][test_id] contenant la sortie
        # des résultats attendus de chaque test
        self.expected_results = self.execute_results()
        # Liste à deux entrées [question_id][test_id] contenant la sortie
        # des résultats obtenus par le fichier réponse de chaque test
        self.obtained_results = []
        # Liste à deux entrées [question_id][test_id] contenant la sortie
        # (stdout) des résultats obtenus par le fichier réponse de chaque test
        self.std_results = []
        # Liste à deux entrées [question_id][test_id] contenant l'état
        # des résultats obtenus : False lorsque le test n'est pas effectué
        self.enabled_results = []
        # Liste à deux entrées [question_id][test_id] contenant le nombre
        # de point obtenus à chaque test
        self.points = []
        # Couleur des questions :
        # vert : tous les points de la question obtenus
        # rouge : moins de la moitié des points obtenus à la question
        # jaune : plus de la moitié des points obtenus à la question
        self.questions_color = []
        # Nombre de points obtenus à chaque questions
        self.mark_question = []
        # Sortie standard après exécution du travail évalué
        self.work_stdout = ""
        self.clear_all()

    def clear_all(self):
        self.work_module = None
        self.obtained_results = []
        self.std_results = []
        self.enabled_results = []
        self.points = []
        for qu_id in range(len(self.expected_results)):
            te = len(self.expected_results[qu_id])
            self.obtained_results.append([None for _ in range(te)])
            self.std_results.append(["" for _ in range(te)])
            self.points.append([0 for _ in range(te)])
            self.enabled_results.append([False for _ in range(te)])
        self.questions_color = ["#DADADA"]*len(self.expected_results)
        self.mark_question = [0]*len(self.expected_results)

    def clear_question(self, question_id):
        te = len(self.expected_results[question_id])
        self.obtained_results[question_id] = [None for _ in range(te)]
        self.std_results[question_id] = ["" for _ in range(te)]
        self.points[question_id] = [0 for _ in range(te)]
        self.enabled_results[question_id] = [False for _ in range(te)]
        self.questions_color[question_id] = "#DADADA"
        self.mark_question[question_id] = 0

    def execute_results(self):
        """
        Un résultat pouvant être une instruction donnant le résultat souhaité,
        cette fonction exécute ce résultat pour obtenir la sortie souhaitée
        Elle renvoie une liste à deux entrées : [question_id][test_id] """
        list_res = []
        for qu in self.session.list_questions:
            list_res_qu = []
            for test in qu.list_tests:
                list_res_qu.append(to.execute(test.get_result(),
                                   test.get_max_time()))
            list_res.append(list_res_qu)
        return list_res

    def import_module_work(self, file_loc):
        """ Execute le fichier situé dans file_loc
        et le charge dans le module dans self.work_module """
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout
        module = to.import_mod(file_loc, self.max_time_import)
        self.work_stdout = new_stdout.getvalue()
        sys.stdout = old_stdout

        if isinstance(module, Exception):
            self.clear_all()
            raise module
        else:
            self.work_module = module

    def is_answered(self, question_id):
        func_name = self.session.get_question_byid(question_id).get_func_name()
        return hasattr(self.work_module, func_name)

    def execute_test(self, test):
        is_varname_changed = False
        for name, inst in test.get_custom_var().items():
            res = to.execute(inst, test.get_max_time())
            # On vérifie si une variable portant le même nom que la
            # variable personnalisée n'existe pas.
            # Si c'est le cas on change le nom de la variable dans le fichier
            # pour ne pas l'écraser (on utilise une fonction de hacjage perso)
            if hasattr(self.work_module, name):
                new_name = "Cust_Var_" + str(Work.hash_string(name))
                is_varname_changed = True
                setattr(self.work_module, new_name,
                        getattr(self.work_module, name))
            setattr(self.work_module, name, res)

        res = to.execute(test.get_command(), test.get_max_time(),
                         {"work_module": self.work_module})

        if is_varname_changed:
            for name in test.get_custom_var():
                new_name = "Cust_Var_" + str(Work.hash_string(name))
                if hasattr(self.work_module, new_name):
                    setattr(self.work_module, name,
                            getattr(self.work_module, new_name))

        return res

    def execute_tests_question(self, question_id):
        self.clear_question(question_id)
        qu = self.session.get_question_byid(question_id)
        no_test = self.work_module is None or not self.is_answered(question_id)
        for test_id in range(qu.get_number_tests()):
            res = None
            if not no_test:
                old_stdout = sys.stdout
                new_stdout = StringIO()
                sys.stdout = new_stdout
                res = self.execute_test(qu.get_test_byid(test_id))
                self.enabled_results[question_id][test_id] = True
                self.std_results[question_id][test_id] = new_stdout.getvalue()
                sys.stdout = old_stdout

            self.obtained_results[question_id][test_id] = res

            if (qu.get_test_byid(test_id).get_level() == "fatal" and
                    not self.is_test_success(question_id, test_id)):
                no_test = True
            if (qu.get_test_byid(test_id).get_level() in {"critic", "error"}
                    and isinstance(res, Exception)):
                no_test = True

    def execute_all_tests(self):
        """ Remplit la liste self.obtained_results """
        for qu_id in range(self.session.get_number_questions()):
            self.execute_tests_question(qu_id)

    def get_expected_result(self, question_id, test_id):
        return Work.show_type_value(
            self.expected_results[question_id][test_id])

    def get_expected_result_value(self, question_id, test_id):
        return self.expected_results[question_id][test_id]

    def get_obtained_result(self, question_id, test_id):
        return Work.show_type_value(
            self.obtained_results[question_id][test_id])

    def get_obtained_result_value(self, question_id, test_id):
        return self.obtained_results[question_id][test_id]

    def get_enabled_result(self, question_id, test_id):
        return self.enabled_results[question_id][test_id]

    def get_std_result(self, question_id, test_id):
        return self.std_results[question_id][test_id]

    def is_test_success(self, question_id, test_id):
        t = self.session.get_question_byid(question_id).get_test_byid(test_id)
        if t.get_level() == "info":
            return False
        ex_res = self.expected_results[question_id][test_id]
        ob_res = self.obtained_results[question_id][test_id]
        if t.get_strict():
            return type(ex_res) == type(ob_res) and ex_res == ob_res
        else:
            return ex_res == ob_res

    def is_test_fail_type(self, question_id, test_id):
        ex_res = self.expected_results[question_id][test_id]
        ob_res = self.obtained_results[question_id][test_id]
        return ex_res == ob_res and type(ex_res) != type(ob_res)

    def is_test_exeption(self, question_id, test_id):
        ob_res = self.obtained_results[question_id][test_id]
        return isinstance(ob_res, Exception)

    def calculate_points_question(self, question_id):
        qu = self.session.get_question_byid(question_id)
        penalty = 0
        all_info = True
        for test_id in range(qu.get_number_tests()):
            if qu.get_test_byid(test_id).get_level() != "info":
                all_info = False
            if self.is_test_success(question_id, test_id):
                point = qu.get_test_byid(test_id).get_point()
            else:
                point = 0
                if qu.get_test_byid(test_id).get_level() == "fatal":
                    penalty = 1
                elif qu.get_test_byid(test_id).get_level() == "critic":
                    penalty = max(0.25, penalty)
            self.points[question_id][test_id] = point

        if all_info:
            mark = qu.get_scale()
        elif not self.is_answered(question_id):
            mark = 0
        else:
            mark = sum(self.points[question_id])
            mark = mark*(1-penalty)*qu.get_scale()/qu.get_total_points_test()
        self.mark_question[question_id] = mark

        if not self.is_answered(question_id):
            self.questions_color[question_id] = "#DADADA"
        elif mark == qu.get_scale():
            self.questions_color[question_id] = "green"
        elif mark > qu.get_scale()/2 - 0.01:
            self.questions_color[question_id] = "orange"
        else:
            self.questions_color[question_id] = "red"

    def calculate_all_points(self):
        for qu_id in range(self.session.get_number_questions()):
            self.calculate_points_question(qu_id)

    def get_total_passed_tests(self):
        s = 0
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                if self.is_test_success(i, j) and self.is_answered(i):
                    s += 1
        return s

    def get_total_passed_questions(self):
        s = 0
        for c in self.questions_color:
            if c == "green":
                s += 1
        return s

    def get_total_mark(self):
        return sum(self.mark_question)

    def get_question_mark(self, question_id):
        return self.mark_question[question_id]

    def get_question_color(self, question_id):
        return self.questions_color[question_id]

    def get_stdout(self):
        return self.work_stdout

    @staticmethod
    def show_type_value(value):
        res = "[" + type(value).__name__ + "] : "
        res += str(value)
        return res

    @staticmethod
    def hash_string(name):
        p = 1
        h = 0
        for c in name:
            h = (h + ord(c)*p) % 9999999929
            p *= 31
        return h
