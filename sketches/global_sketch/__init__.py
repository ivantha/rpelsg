from _datetime import datetime

from .table import Table
from ..utils import get_files, get_lines

base_path: str = None
streaming_path: str = None

table: Table = None


def init_environment(base_dir_path: str, streaming_dir_path: str, m: int = 1048576, d: int = 5):
    """
    Initialize the environment
    :param base_dir_path:
    :param streaming_dir_path:
    :param m: Size of the hash tables
    :param d: Number of hash tables
    """
    global base_path
    global streaming_path

    global table

    base_path = base_dir_path
    streaming_path = streaming_dir_path

    table = Table(m, d)


def construct_base_graph():
    return _stream(base_path)


def stream_edges():
    return _stream(streaming_path)


def print_analytics():
    return table.print_analytics()


def _stream(path: str):
    start_time = datetime.now()

    data_files = get_files(path)
    for data_file in data_files:
        for line in get_lines(data_file):
            source_id, target_id, _ = line.split()
            table.add_edge('{},{}'.format(source_id, target_id))

    end_time = datetime.now()

    return start_time, end_time
