import hashlib

import numpy as np
from pympler import asizeof

from common.utils import timeit
from sketches import Sketches
from sketches.sketch import Sketch


class TcmTable:
    def __init__(
            self,
            w: int,  # w: Size of the hash table
            d: int  # d: Number of hash functions
    ):
        self._w = w
        self._d = d

        self.edge_count: int = 0
        self.matrix = np.zeros((d, w, w))

    def add_edge(self, x: str, y: str):
        new_buckets_occupied = 0

        for i, x_hash, y_hash in zip(range(self._d), self._hash(x), self._hash(y)):
            if self.matrix[i][x_hash][y_hash] == 0:
                new_buckets_occupied += 1
            self.matrix[i][x_hash][y_hash] += 1
        self.edge_count += 1

        return new_buckets_occupied

    def get_edge_frequency(self, x: str, y: str):
        return min([self.matrix[i][x_hash][y_hash] for i, x_hash, y_hash in zip(range(self._d), self._hash(x), self._hash(y))])

    def _hash(self, x: str):
        x_hash = hashlib.md5(str(hash(x)).encode('utf-8'))
        for i in range(self._d):
            x_hash.update(str(i).encode('utf-8'))
            yield int(x_hash.hexdigest(), 16) % self._w


class TCM(Sketch):
    name = Sketches.tcm.name

    def __init__(
            self,
            # [INT_SIZE * w * w * d]
            # [2 bytes * (181 * 181) * 8 = 511 KB)]
            w: int,  # w: Side width of the hash tables (size = w * w)
            d: int  # d: Number of hash functions
    ):
        self._w = w
        self._d = d

        self._table = None

    @timeit
    def initialize(self):
        self.total_buckets = self._w * self._w * self._d
        self.used_buckets = 0

        self._table = TcmTable(self._w, self._d)

    def add_edge(self, source_id, target_id):
        new_buckets_occupied = self._table.add_edge(source_id, target_id)
        self.used_buckets += new_buckets_occupied

    def get_edge_frequency(self, source_id, target_id):
        return self._table.get_edge_frequency(source_id, target_id)

    @timeit
    def print_analytics(self):
        print('Bucket ratio (used/total) : {:,}/{:,} ({}%)'.format(self.used_buckets, self.total_buckets, self.used_buckets / self.total_buckets * 100.0))

        # return {
        #     'edge_count': self._table.edge_count,
        #     'table_object_size': asizeof.asizeof(self._table.matrix)
        # }
