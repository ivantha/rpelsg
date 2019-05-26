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

    def __init__(self, base_path: str, streaming_path: str, m: int = 1048576, d: int = 5):
        """
        :param base_path:
        :param streaming_path:
        :param m: Size of the hash tables
        :param d: Number of hash tables
        """
        super().__init__(base_path, streaming_path)

        self._table = Table(m, d)

    @timeit
    def construct_base_graph(self):
        self._stream(self.base_path, self._edge_fun)

    @timeit
    def construct_stream_graph(self):
        self._stream(self.streaming_path, self._edge_fun)

    @timeit
    def print_analytics(self):
        print('Edge count: {:,}'.format(self._table._edge_count))
        print('Table object size: {} bytes ({:.4f} MB)'.format(asizeof.asizeof(self._table._tables),
                                                               asizeof.asizeof(self._table._tables) / 1024.0 / 1024.0))

    def _edge_fun(self, source_id, target_id):
        self._table.add_edge('{},{}'.format(source_id, target_id))
