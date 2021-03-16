"""
    Implement a decorator that counts the number of calls for each
    function it decorates
"""

import functools


def counter_decorator(f):

    counter = 0

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)

        nonlocal counter
        counter += 1
        print(f'{f.__name__} function was called {counter} times')

    return wrapper


# --------------------------------------------------------------------
# Tests

@counter_decorator
def say_hello():
    print("Hello")


@counter_decorator
def say_goodbye():
    print("Goodbye")


say_hello()
say_goodbye()
say_hello()
say_hello()
say_goodbye()


