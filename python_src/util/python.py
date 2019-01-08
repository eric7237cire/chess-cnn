import functools
import logging
import sys
from time import sleep


def init_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    #ch.setLevel(logging.ERROR)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.INFO)

    if False:
        logging.getLogger("card_classifier_trace").setLevel(logging.INFO)
        logging.getLogger("number_reader").setLevel(logging.INFO)

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
