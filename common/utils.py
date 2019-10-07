import glob
from _datetime import datetime


def get_txt_files(dir_path: str):
    return [f for f in glob.glob(dir_path + '*.txt', recursive=True)]


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        if result is None:
            return start_time, end_time
        else:
            return start_time, end_time, result

    return wrapper
