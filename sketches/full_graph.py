from typing import Dict, List

from pympler import asizeof

from common.utils import timeit
from sketches import Sketches
from sketches.sketch import Sketch


class Node:
    def __init__(self, id: str):
        self._id = id


class Graph:
    def __init__(self):
        self._nodes: Dict[str, Node] = {}
        self._node_count: int = 0

        self._edges: Dict[str, Dict] = {}
        self._edge_count: int = 0

    def add_node(self, node_id: str):
        if node_id not in self._nodes:
            self._nodes[node_id] = Node(node_id)
            self._node_count += 1

            self._edges[node_id] = {}

    def add_edge(self, source_id: str, target_id: str):
        if target_id not in self._edges[source_id]:
            self._edges[source_id][target_id] = 0
        self._edges[source_id][target_id] += 1
        self._edge_count += 1


class FullGraph(Sketch):
    name = Sketches.fullgraph.name

    def __init__(self):
        self.graph = None

    @timeit
    def initialize(self):
        self.graph = Graph()

    def add_edge(self, source_id, target_id):
        self.graph.add_node(source_id)
        self.graph.add_node(target_id)
        self.graph.add_edge(source_id, target_id)

    def get_edge_frequency(self, source_id, target_id):
        return self.graph._edges[source_id][target_id]

    @timeit
    def get_analytics(self):
        return {
            'node_count': self.graph._node_count,
            'edge_count': self.graph._edge_count,
            'node_store_size': asizeof.asizeof(self.graph._nodes),
            'edge_store_size': asizeof.asizeof(self.graph._edges),
            'graph_object_size': asizeof.asizeof(self)
        }
