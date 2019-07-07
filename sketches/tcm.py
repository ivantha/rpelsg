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

    def _hash(self, v: str):
        v_hash = hashlib.md5(str(hash(v)).encode('utf-8'))
        for i in range(self.d):
            v_hash.update(str(i).encode('utf-8'))
            yield int(v_hash.hexdigest(), 16) % self.d


class TCM(Sketch):

    def __init__(
            self,
            base_path: str,
            streaming_path: str,
            w: int = 1024,
            d: int = 5
    ):
        """
        :param base_path:
        :param streaming_path:
        :param w: Size of the hash tables (side width)
        :param d: Number of hash functions
        """
        super().__init__(base_path, streaming_path)

        self.table = Table(w, d)

    @timeit
    def construct_base_graph(self):
        self._stream(self.base_path, self._edge_fun)

    @timeit
    def construct_stream_graph(self):
        self._stream(self.streaming_path, self._edge_fun)

    @timeit
    def print_analytics(self):
        print('Edge count: {:,}'.format(self.table.edge_count))
        print('Table object size: {} bytes ({:.4f} MB)'.format(asizeof.asizeof(self.table.matrix),
                                                               asizeof.asizeof(self.table.matrix) / 1024.0 / 1024.0))

    def _edge_fun(self, source_id, target_id):
        self.table.add_edge(source_id, target_id)