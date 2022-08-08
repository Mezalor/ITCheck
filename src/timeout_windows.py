import importlib.util
import ctypes
import random
import sys
import threading
import time

_set_async_exc = ctypes.pythonapi.PyThreadState_SetAsyncExc
_set_async_exc.argtypes = (ctypes.c_ulong, ctypes.py_object)
_system_exit = ctypes.py_object(SystemExit)


class UninterruptableImport(ImportError):
    pass


class TimeoutException(Exception):
    pass


class NonePythonFileException(Exception):
    pass


class TimeLimitedImporter():
    def __init__(self, modulename, timeout=2):
        self.modulename = modulename
        self.module = None
        self.exception = None
        self.timeout = timeout

        self._started = None
        self._started_event = threading.Event()
        self._importer = threading.Thread(target=self._import, daemon=True)
        self._importer.start()
        self._started_event.wait()

    def _import(self):
        self._started = time.time()
        self._started_event.set()
        timer = threading.Timer(self.timeout, self.exit)
        timer.start()
        try:
            spec = importlib.util.spec_from_file_location("wm",
                                                          self.modulename)
            if spec is None:
                raise NonePythonFileException("Problème d'importation "
                                              + "du fichier Python")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.module = mod
        except Exception as e:
            self.exception = e
        finally:
            timer.cancel()

    def result(self, timeout=None):
        # give the importer a chance to finish first
        if timeout is not None:
            timeout += max(time.time() + self.timeout - self._started, 0)
        self._importer.join(timeout)
        if self._importer.is_alive():
            raise UninterruptableImport(
                f"Could not interrupt the import of {self.modulename}")
        if self.module is not None:
            return self.module
        if self.exception is not None:
            raise self.exception

    def exit(self):
        self.exception = TimeoutException("temps dépassé ("
                                          + str(self.timeout) + "s)")
        target_id = self._importer.ident
        if target_id is None:
            return
        # set a very low switch interval to be able to interrupt an exception
        # handler if SystemExit is being caught
        old_interval = sys.getswitchinterval()
        sys.setswitchinterval(1e-6)

        try:
            # repeatedly raise SystemExit until the import thread has exited.
            # If the exception is being caught by a an exception handler,
            # our only hope is to raise it again *while inside the handler*
            while True:
                _set_async_exc(target_id, _system_exit)

                # short randomised wait times to 'surprise' an exception
                # handler
                self._importer.join(
                    timeout=random.uniform(1e-4, 1e-5)
                )
                if not self._importer.is_alive():
                    return
        finally:
            sys.setswitchinterval(old_interval)


class TimeLimitedExec():
    def __init__(self, command, globals_var={}, timeout=1):
        self.command = command
        self.globals_var = globals_var
        self.result = None
        self.exception = None
        self.timeout = timeout

        self._started = None
        self._started_event = threading.Event()
        self._execute = threading.Thread(target=self._exec, daemon=True)
        self._execute.start()
        self._started_event.wait()

    def _exec(self):
        self._started = time.time()
        self._started_event.set()
        timer = threading.Timer(self.timeout, self.exit)
        timer.start()
        try:
            loc = {}
            exec("result = " + str(self.command), self.globals_var, loc)
            self.result = loc['result']
        except Exception as e:
            self.exception = e
        finally:
            timer.cancel()

    def get_result(self, timeout=None):
        # give the importer a chance to finish first
        if timeout is not None:
            timeout += max(time.time() + self.timeout - self._started, 0)
        self._execute.join(timeout)
        if self._execute.is_alive():
            raise UninterruptableImport(
                f"Could not interrupt the execution of {self.command}")
        if self.result is not None:
            return self.result
        if self.exception is not None:
            raise self.exception

    def exit(self):
        self.exception = TimeoutException("temps dépassé ("
                                          + str(self.timeout) + "s)")
        target_id = self._execute.ident
        if target_id is None:
            return
        # set a very low switch interval to be able to interrupt an exception
        # handler if SystemExit is being caught
        old_interval = sys.getswitchinterval()
        sys.setswitchinterval(1e-6)

        try:
            # repeatedly raise SystemExit until the import thread has exited.
            # If the exception is being caught by a an exception handler,
            # our only hope is to raise it again *while inside the handler*
            while True:
                _set_async_exc(target_id, _system_exit)

                # short randomised wait times to 'surprise' an exception
                # handler
                self._execute.join(
                    timeout=random.uniform(1e-4, 1e-5)
                )
                if not self._execute.is_alive():
                    return
        finally:
            sys.setswitchinterval(old_interval)


def import_mod(file_loc, max_time_import):
    """ Execute le fichier situé dans file_loc, le charge
        et renvoie le module associé """
    try:
        importer = TimeLimitedImporter(file_loc, max_time_import)
        return importer.result(0.1)
    except Exception as err:
        return err


def execute(command, max_time=1, globals_var={}):
    try:
        ex = TimeLimitedExec(command, globals_var, max_time)
        return ex.get_result(0.1)
    except Exception as err:
        return err
