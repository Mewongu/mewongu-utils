# utils.py
# Andreas Stenberg

from time import time


class timed_ctx:
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

