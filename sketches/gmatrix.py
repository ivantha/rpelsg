import random

import numpy as np

from common.utils import timeit
from sketches import Sketches
from sketches.sketch import Sketch


class GMatrixTable:
    def __init__(
            self,
            w: int,  # w: Size of the hash table
            d: int  # d: Number of hash functions
    ):
        self.w = w
        self.d = d

        self.edge_count: int = 0
        self.matrix = np.zeros((d, w, w))

        # P = 2^31 - 1 = 2147483647
        self.P = 2147483647
        self.a = [random.randrange(1, self.P) for i in range(d)]
        self.b = [random.randrange(1, self.P) for i in range(d)]

    def add_edge(self, x: str, y: str):
        for i, x_hash, y_hash in zip(range(self.d), self._hash(x), self._hash(y)):
            self.matrix[i][x_hash][y_hash] += 1
        self.edge_count += 1

    def get_edge_frequency(self, x: str, y: str):
        return min([self.matrix[i][x_hash][y_hash] for i, x_hash, y_hash in zip(range(self.d), self._hash(x), self._hash(y))])

    def _hash(self, x: str):
        x_int = int(x)
        for i in range(self.d):
            yield (((self.a[i] * x_int) + self.b[i]) % self.P) % self.w


class GMatrix(Sketch):
    name = Sketches.gmatrix.name

    def __init__(
            self,
            # [INT_SIZE * w * w * d]
            # [2 bytes * (181 * 181) * 8 = 511 KB)]
            w: int,  # w: Side width of the hash tables (size = ↓w * →w)
            d: int  # d: Number of hash functions
    ):
        self.w = w
        self.d = d

        self.table = None

    @timeit
    def initialize(self):
        self.table = GMatrixTable(self.w, self.d)

    def add_edge(self, source_id, target_id):
        self.table.add_edge(source_id, target_id)

    def get_edge_frequency(self, source_id, target_id):
        return self.table.get_edge_frequency(source_id, target_id)

    @timeit
    def print_analytics(self):
        pass

        # return {
        #     'edge_count': self._table.edge_count,
        #     'table_object_size': asizeof.asizeof(self._table.matrix)
        # }
