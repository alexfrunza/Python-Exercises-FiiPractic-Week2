"""
    Implement a decorator which retries the following function
    if it returns False
"""

import functools
import random


def repetitive_decorator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        while not f(*args, **kwargs):
            pass

        return True

    return wrapper


# --------------------------------------------------------------------
# Tests

@repetitive_decorator
def get_random_bool():
    return random.randint(0, 100) < 50
