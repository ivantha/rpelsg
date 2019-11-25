from abc import ABC, abstractmethod
from typing import List

from p_tqdm import p_umap

from common.utils import timeit


class Sketch(ABC):
    name: str

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def add_edge(self, source_id, target_id):
        pass

    @abstractmethod
    def get_edge_frequency(self, source_id, target_id):
        pass

    @abstractmethod
    def get_analytics(self):
        pass

    @timeit
    def stream(self, edges: List):
        def stream_edge(edge):
            self.add_edge(edge[0], edge[1])

        # parallel edge streaming
        p_umap(stream_edge, edges)
