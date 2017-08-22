# utils.py
# Author: Andreas Stenberg

from time import time
from functools import wraps


class timed_ctx:
    """
    Context manager for timing a block of code
    """
    def __init__(self, msg='Elapsed time:', log_func=None):
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
        self.log_func = log_func
        self.msg = msg

    def __call__(self, fn):
        @wraps(fn)
        def fn_call(*args, **kwargs):
            with timed_ctx(msg=self.msg, log_func=self.log_func):
                return fn(*args, **kwargs)
        return fn_call

