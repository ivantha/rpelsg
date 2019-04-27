import glob


def get_files(dir_path: str):
    return [f for f in glob.glob(dir_path + '*.txt', recursive=True)]


def get_lines(file_path: str):
    f = open(file_path)
    return f.readlines()
