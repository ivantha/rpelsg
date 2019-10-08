import hashlib

import numpy as np
from pympler import asizeof

from common.utils import timeit
from sketches.sketch import Sketch


class Table:

    def __init__(self, m: int, d: int):
        """
        :param m: Size of the hash tables
        :param d: Number of hash functions
        """
        self.m = m
        self.d = d
        self._edge_count: int = 0

        self._tables = np.zeros((d, m))  # d rows ; m cols

    def add_edge(self, x: str):
        for i, x_hash in zip(range(self.d), self._hash(x)):
            self._tables[i][x_hash] += 1
        self._edge_count += 1

    def _hash(self, x: str):
        x_hash = hashlib.md5(str(hash(x)).encode('utf-8'))
        for i in range(self.d):
            x_hash.update(str(i).encode('utf-8'))
            yield int(x_hash.hexdigest(), 16) % self.m


class GlobalCountMin(Sketch):

    def __init__(self, m: int = 1048576, d: int = 5):
        """
        :param m: Size of the hash tables
        :param d: Number of hash tables
        """
        self.m = m
        self.d = d

        self._table = None

    @timeit
    def initialize(self):
        self._table = Table(self.m, self.d)

    def add_edge(self, source_id, target_id):
        self._table.add_edge('{},{}'.format(source_id, target_id))

    def get_edge_frequency(self, source_id, target_id):
        pass

    @timeit
    def get_analytics(self):
        return {
            'edge_count': self._table._edge_count,
            'table_object_size': asizeof.asizeof(self._table._tables)
        }
