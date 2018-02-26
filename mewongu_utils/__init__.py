# mewongu_utils
# Author: Andreas Stenberg
import cProfile
import collections
import pstats
from collections import MutableMapping
from time import time, sleep
from functools import wraps
import os


class timed_ctx:
    """
    Context manager for timing a block of code
    """
    def __init__(self, msg='Elapsed time:', log_func=None):
        """
        :param msg: The message to display before the time
        :param log_func: The function to call with the full message. Must handle a single string argument
        """
        self.log_func = log_func
        self.msg = msg

    def __enter__(self):
        self.time = time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.log_func:
            self.log_func(f'{self.msg} {time()-self.time}')
        else:
            print(f'{self.msg} {time()-self.time}')


class timed:
    """
    Decorator for timing a function call
    """
    def __init__(self, msg='Elapsed time:', log_func=None):
        """
        :param msg: The message to display before the time
        :param log_func: The function to call with the full message. Must handle a single string argument
        """
        self.log_func = log_func
        self.msg = msg

    def __call__(self, fn):
        @wraps(fn)
        def fn_call(*args, **kwargs):
            with timed_ctx(msg=self.msg, log_func=self.log_func):
                return fn(*args, **kwargs)
        return fn_call


def tail(filename, check_interval=1):
    """
    Tail a file checking for changes
    :param filename: The file to tail
    :param check_interval: How often should it be rechecked? default: 1 second
    :return: yields the file line by line
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(filename)
    last_pos = 0
    while True:
        try:
            with open(filename, 'r') as fin:
                fin.seek(last_pos)
                res = True
                while res:
                    res = fin.readline().rstrip()
                    if res:
                        yield res
                last_pos = fin.tell()
        except FileNotFoundError:
            pass
        finally:
            sleep(check_interval)


class KeyChangeDict(dict):
    """
    A class that allows you to extend it and modify key behaviour in dicts
    """
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        return super(KeyChangeDict, self).__getitem__(self._key_modifier(key))

    def __setitem__(self, key, value):
        return super(KeyChangeDict, self).__setitem__(self._key_modifier(key), value)

    def __delitem__(self, key):
        return super(KeyChangeDict, self).__delitem__(self._key_modifier(key))

    def get(self, key, default=None):
        return super(KeyChangeDict, self).get(self._key_modifier(key), default)

    def setdefault(self, key, default=None):
        return super(KeyChangeDict, self).setdefault(self._key_modifier(key), default)

    def pop(self, key):
        return super(KeyChangeDict, self).pop(self._key_modifier(key))

    def __contains__(self, key):
        return super(KeyChangeDict, self).__contains__(self._key_modifier(key))

    def copy(self):
        return type(self)(self)

    def _key_modifier(self, key):
        return key


class profiled_ctx:
    def __init__(self, file_name, directory=None):
        self.file_name = file_name
        self.directory = directory or './'
        self.pr = cProfile.Profile()

    def __enter__(self):
        self.pr.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pr.disable()
        file_path = os.path.join(self.directory, f'{self.file_name}.pstat')
        pstats.Stats(self.pr).dump_stats(file_path)

