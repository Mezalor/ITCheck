import importlib
import signal
from contextlib import contextmanager


class Work:

    def __init__(self, session, file_loc="", max_time_import=2,
                 max_time_result=1):
        """
        session : Objet de type model.Session contenant le sujet du TP :
                  ie les questions et tests à réaliser
        file_loc : chemin du fichier réponse (fichier python où se
                                               trouve les fonctions à tester)
        max_time_import : temps maximal en sec pour l'importation du fichier
        max_time_import : temps maximal en sec pour calculer chaque résultat
        """
        self.session = session
        self.file_loc = file_loc
        self.max_time_import = max_time_import
        self.max_time_result = max_time_result
        # Le module contenant les fonctions du travail évalué
        self.work_module = None
        # Liste à deux entrées [question_id][test_id] contenant la sortie
        # des résultats attendus de chaque test
        self.expected_results = self.execute_results()
        # Liste à deux entrées [question_id][test_id] contenant le sortie
        # des résultats obtenus par le fichier réponse de chaque test
        self.obtained_results = []
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
        self.clear_all()

    def execute_results(self):
        """
        Un résultat pouvant être une instruction donnant le résultat souhaité,
        cette fonction exécute ce résultat pour obtenir la sortie souhaitée
        Elle renvoie une liste à deux entrées : [question_id][test_id] """
        list_res = []
        for qu in self.session.list_questions:
            list_res_qu = []
            for test in qu.list_tests:
                list_res_qu.append(Work.execute(test.get_result(),
                                   self.max_time_result))
            list_res.append(list_res_qu)
        return list_res

    def clear_all(self):
        self.work_module = None
        self.obtained_results = []
        self.points = []
        for qu_id in range(len(self.expected_results)):
            te = len(self.expected_results[qu_id])
            self.obtained_results.append([None for _ in range(te)])
            self.points.append([0 for _ in range(te)])
        self.questions_color = ["#DADADA"]*len(self.expected_results)
        self.mark_question = [0]*len(self.expected_results)

    def import_module_work(self, file_loc):
        """ Execute le fichier situé dans file_loc
            et le charge dans le module dans self.work_module """
        try:
            spec = importlib.util.spec_from_file_location("wm", file_loc)
            module = importlib.util.module_from_spec(spec)
            with timeout(self.max_time_import):
                spec.loader.exec_module(module)
            self.work_module = module
        except Exception as err:
            self.clear_all()
            raise err

    def is_answered(self, question_id):
        func_name = self.session.get_question_byid(question_id).get_func_name()
        return hasattr(self.work_module, func_name)

    # C'est très moche à revoir !
    def execute_test(self, test):
        for name, inst in test.get_custom_var().items():
            res = Work.execute(inst, test.get_max_time())
            # Le hachage du pauvre ...
            new_name = (name + "W_K_Z_q_x_j")*3
            if name == "dist":
                a = 2
                a += 1
            if hasattr(self.work_module, name):
                setattr(self.work_module, new_name,
                        getattr(self.work_module, name))
            setattr(self.work_module, name, res)
        res = Work.execute(test.get_command(), test.get_max_time(),
                           {"work_module": self.work_module})
        for name in test.get_custom_var():
            new_name = (name + "W_K_Z_q_x_j")*3
            if hasattr(self.work_module, new_name):
                setattr(self.work_module, name,
                        getattr(self.work_module, new_name))

        return res

    def execute_tests_question(self, question_id):
        qu = self.session.get_question_byid(question_id)
        no_test = False
        for test_id in range(qu.get_number_tests()):
            res = None
            if not no_test:
                res = self.execute_test(qu.get_test_byid(test_id))

            if (qu.get_test_byid(test_id).get_level() == "fatal" and
                    res != self.expected_results[question_id][test_id]):
                no_test = True
            if (qu.get_test_byid(test_id).get_level() == "critic" and
                    isinstance(res, Exception)):
                no_test = True

            self.obtained_results[question_id][test_id] = res

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

    def is_test_success(self, question_id, test_id):
        ex_res = self.expected_results[question_id][test_id]
        ob_res = self.obtained_results[question_id][test_id]
        return ex_res == ob_res

    # TODO : Gerer le calcul des points avec les level
    def calculate_points_question(self, question_id):
        qu = self.session.get_question_byid(question_id)
        for test_id in range(qu.get_number_tests()):
            if self.is_test_success(question_id, test_id):
                point = qu.get_test_byid(test_id).get_point()
            else:
                point = 0
            self.points[question_id][test_id] = point
        mark = sum(self.points[question_id])
        mark = mark*qu.get_scale()/qu.get_total_points_test()
        self.mark_question[question_id] = mark
        if not self.is_answered(question_id):
            self.questions_color[question_id] = "#DADADA"
        elif mark == qu.get_scale():
            self.questions_color[question_id] = "green"
        elif mark > qu.get_scale()/2:
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
                if self.is_test_success(i, j):
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

    @staticmethod
    def execute(command, max_time=1, globals_var={}):
        loc = {}
        try:
            with timeout(max_time):
                exec("result = " + str(command), globals_var, loc)
        except Exception as err:
            loc['result'] = err
        return loc['result']

    @staticmethod
    def show_type_value(value):
        res = "[" + type(value).__name__ + "] : "
        res += str(value)
        return res


# CLasse d'exceptions :
# TimeoutException : en cas de dépassement du temps d'exécution

class TimeoutException(Exception):
    pass


@contextmanager
def timeout(seconds):

    def signal_handler(signum, frame):
        raise TimeoutException("temps dépassé (" + str(seconds) + "s)")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)

    try:
        yield
    except TimeoutException:
        raise
    finally:
        signal.alarm(0)
