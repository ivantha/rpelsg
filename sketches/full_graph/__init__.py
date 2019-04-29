from _datetime import datetime

from .graph import Graph
from ..utils import get_files, get_lines

graph: Graph = None
base_path: str = None
streaming_path: str = None


def init_environment(base_dir_path: str, streaming_dir_path: str):
    global graph
    global base_path
    global streaming_path

    graph = Graph()
    base_path = base_dir_path
    streaming_path = streaming_dir_path


def construct_base_graph():
    return _stream(base_path)


def stream_edges():
    return _stream(streaming_path)


def print_analytics():
    return graph.print_analytics()


def _stream(path: str):
    start_time = datetime.now()

    data_files = get_files(path)
    for data_file in data_files:
        for line in get_lines(data_file):
            source_id, target_id, _ = line.split()

            graph.add_node(source_id)
            graph.add_node(target_id)

            assert source_id in graph._nodes, 'source_id "{}" not found'.format(source_id)
            assert target_id in graph._nodes, 'target_id "{}" not found'.format(target_id)
            graph.add_edge(source_id, target_id)

    end_time = datetime.now()

    return start_time, end_time
