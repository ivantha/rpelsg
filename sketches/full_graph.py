from typing import Dict, List

from pympler import asizeof

from common.utils import timeit
from sketches.sketch import Sketch


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

    @timeit
    def construct_base_graph(self):
        self._stream(self.base_path, self._edge_fun)

    @timeit
    def construct_stream_graph(self):
        self._stream(self.streaming_path, self._edge_fun)

    @timeit
    def print_analytics(self, file):
        file.write('\nNode count: {:,}\n'.format(self.graph._node_count))
        file.write('Edge count: {:,}\n'.format(self.graph._edge_count))
        file.write('Node store size: {} bytes ({:.4f} MB)\n'.format(asizeof.asizeof(self.graph._nodes),
                                                             asizeof.asizeof(self.graph._nodes) / 1024.0 / 1024.0))
        file.write('Edge store size: {} bytes ({:.4f} MB)\n'.format(asizeof.asizeof(self.graph._edges),
                                                             asizeof.asizeof(self.graph._edges) / 1024.0 / 1024.0))
        file.write('Graph object size: {} bytes ({:.4f} MB)\n'.format(asizeof.asizeof(self),
                                                               asizeof.asizeof(self) / 1024.0 / 1024.0))

    def _edge_fun(self, source_id, target_id):
        self.graph.add_node(source_id)
        self.graph.add_node(target_id)

        assert source_id in self.graph._nodes, 'source_id "{}" not found'.format(source_id)
        assert target_id in self.graph._nodes, 'target_id "{}" not found'.format(target_id)
        self.graph.add_edge(source_id, target_id)
