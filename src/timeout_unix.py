import importlib.util
import signal
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


class NonePythonFileException(Exception):
    pass


def import_mod(file_loc, max_time_import):
    """ Execute le fichier situé dans file_loc, le charge
        et renvoie le module associé """
    try:
        spec = importlib.util.spec_from_file_location("wm", file_loc)
        if spec is None:
            raise NonePythonFileException("Problème d'importation "
                                          + "du fichier Python")
        module = importlib.util.module_from_spec(spec)
        with timeout(max_time_import):
            spec.loader.exec_module(module)
        return module
    except Exception as err:
        return err


def execute(command, max_time=1, globals_var={}):
    loc = {}
    try:
        with timeout(max_time):
            exec("result = " + str(command), globals_var, loc)
    except Exception as err:
        loc['result'] = err
    return loc['result']


@contextmanager
def timeout(seconds):
    if seconds < 1:
        seconds = 1
    else:
        seconds = int(seconds)

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
