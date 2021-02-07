import glob
from _datetime import datetime


def get_txt_files(dir_path: str):
    return [f for f in glob.glob(dir_path + '*.txt', recursive=True)]


def get_edges_in_path(path: str):
    edges = []
    for i, data_file in enumerate(get_txt_files(path)):
        with open(data_file) as file:
            for line in file.readlines():
                try:
                    source_id, target_id = line.strip().split(',')
                    edges.append((source_id, target_id))
                except:
                    print('Erroneous input: {}'.format(line))

    return edges


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


# print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()