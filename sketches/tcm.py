import hashlib

import numpy as np
from pympler import asizeof

from common.utils import timeit
from sketches.sketch import Sketch


class Table:

    def __init__(self, w: int, d: int):
        """
        :param w: Size of the hash table
        :param d: Number of hash functions
        """
        self.w = w
        self.d = d
        self.edge_count: int = 0

        self.matrix = np.zeros((d, w, w))

    def add_edge(self, x: str, y: str):
        for i, x_hash, y_hash in zip(range(self.d), self._hash(x), self._hash(y)):
            self.matrix[i][x_hash][y_hash] += 1
        self.edge_count += 1

    def get_edge_frequency(self, x: str, y: str):
        return min([self.matrix[i][x_hash][y_hash] for i, x_hash, y_hash in zip(range(self.d), self._hash(x), self._hash(y))])

    def _hash(self, v: str):
        v_hash = hashlib.md5(str(hash(v)).encode('utf-8'))
        for i in range(self.d):
            v_hash.update(str(i).encode('utf-8'))
            yield int(v_hash.hexdigest(), 16) % self.d


class TCM(Sketch):

    def __init__(
            self,
            w: int = 1024,
            d: int = 5
    ):
        """
        :param w: Size of the hash tables (side width)
        :param d: Number of hash functions
        """
        self.w = w
        self.d = d

        self._table = None

    @timeit
    def initialize(self):
        self._table = Table(self.w, self.d)

    def add_edge(self, source_id, target_id):
        self._table.add_edge(source_id, target_id)

    def get_edge_frequency(self, source_id, target_id):
        return self._table.get_edge_frequency(source_id, target_id)

    @timeit
    def get_analytics(self):
        return {
            'edge_count': self._table.edge_count,
            'table_object_size': asizeof.asizeof(self._table.matrix)
        }
