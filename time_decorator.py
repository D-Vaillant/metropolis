# It's just a function mixin, I think. It's a function that wraps around another function.
from functools import wraps

def add_time(func, interval):
    def time_added_func(self, *args, **kwargs):
        func(self, *args, **kwargs)



