import functools
from time import sleep


def retry(retry_count=5, delay=5, allowed_exceptions=()):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for _ in range(retry_count):
                # everything in here would be the same
                try:
                    result = f(*args, **kwargs)
                    if result:
                        return result
                    else:
                        return None
                except allowed_exceptions as e:
                    pass

                print(f"waiting for {delay} seconds before retyring again")
                sleep(delay)

        return wrapper

    return decorator
