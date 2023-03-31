"""
Module that contains the timer decorator.
"""

import time

def timer(func):
    """
    Decorator to time how long a function takes to execute.
    """
    def time_func(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Finished {func.__name__} in {end_time-start_time} seconds")
        return value
    return time_func
