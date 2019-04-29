from _datetime import datetime
from typing import Dict, List

from pympler import asizeof

from sketches.sketch import Sketch
from utils import get_txt_files, get_lines


class Node:

    def __init__(self, id: str):
        self._id = id


class Graph:

    def __init__(self):
        self._nodes: Dict[str, Node] = {}
        self._node_count: int = 0

        self._edges: Dict[str, List] = {}
        self._edge_count: int = 0

    def add_node(self, node_id: str):
        if node_id not in self._nodes:
            self._nodes[node_id] = Node(node_id)
            self._node_count += 1

            self._edges[node_id] = []

    def add_edge(self, source_id: str, target_id: str):
        self._edges[source_id].append(target_id)
        self._edge_count += 1


class FullGraph(Sketch):

    def __init__(self, base_path, streaming_path):
        super().__init__(base_path, streaming_path)

        self.graph = Graph()

    def print_analytics(self):
        start_time = datetime.now()

        print('Node count: {:,}'.format(self.graph._node_count))
        print('Edge count: {:,}'.format(self.graph._edge_count))
        print('Node store size: {} bytes ({:.4f} MB)'.format(asizeof.asizeof(self.graph._nodes),
                                                             asizeof.asizeof(self.graph._nodes) / 1024.0 / 1024.0))
        print('Edge store size: {} bytes ({:.4f} MB)'.format(asizeof.asizeof(self.graph._edges),
                                                             asizeof.asizeof(self.graph._edges) / 1024.0 / 1024.0))
        print('Graph object size: {} bytes ({:.4f} MB)'.format(asizeof.asizeof(self),
                                                               asizeof.asizeof(self) / 1024.0 / 1024.0))

        end_time = datetime.now()

        return start_time, end_time

    def _stream(self, path: str):
        start_time = datetime.now()

        data_files = get_txt_files(path)
        for data_file in data_files:
            for line in get_lines(data_file):
                source_id, target_id = line.split()

                self.graph.add_node(source_id)
                self.graph.add_node(target_id)

                assert source_id in self.graph._nodes, 'source_id "{}" not found'.format(source_id)
                assert target_id in self.graph._nodes, 'target_id "{}" not found'.format(target_id)
                self.graph.add_edge(source_id, target_id)

        end_time = datetime.now()

        return start_time, end_time
