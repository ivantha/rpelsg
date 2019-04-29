from _datetime import datetime
from typing import Dict, List

from pympler import asizeof


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

    def print_analytics(self):
        start_time = datetime.now()

        print('Node count: {:,}'.format(self._node_count))
        print('Edge count: {:,}'.format(self._edge_count))
        print('Graph object size: {} bytes ({:.4f} MB)'.format(asizeof.asizeof(self),
                                                               asizeof.asizeof(self) / 1024.0 / 1024.0))

        end_time = datetime.now()

        return start_time, end_time
