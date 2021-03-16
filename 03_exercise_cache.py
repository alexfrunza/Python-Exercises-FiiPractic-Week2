"""
    Implement a decorator that caches the return of a function.
    Add the ability to select the expiry time of the cache.
    You can use RAM as cache or an external service (ex: Redis, etc)
"""
import functools
import time
import random


def cache_decorator(expire_time):
    def decorator(f):

        saved_content = None
        time_when_saved = 0

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal saved_content
            nonlocal time_when_saved
            delta_time = time.time() - time_when_saved if time_when_saved else expire_time

            if not saved_content or delta_time >= expire_time:
                saved_content = f(*args, **kwargs)
                time_when_saved = time.time()

            return saved_content

        return wrapper

    return decorator


# --------------------------------------------------------------------
# Tests

@cache_decorator(15)
def generate_numbers():
    return [random.randint(0, 100) for _ in range(1000)]


generate_numbers_old = generate_numbers()
print(generate_numbers_old == generate_numbers())

time.sleep(15)

print(generate_numbers_old == generate_numbers())

