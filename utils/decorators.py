import logging
import time


def timeit(f):

    def func(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        logging.info(f">> Finished running {f.__name__}({args}). Runtime: {round(time.time() - start_time, 2)}")
        return result
    return func
