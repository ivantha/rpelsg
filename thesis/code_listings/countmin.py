import hashlib

import numpy as np

from common.utils import timeit
from sketches import Sketches
from sketches.sketch import Sketch


class CountMinTable:
    def __init__(
            self,
            m: int,  # m: Size of the hash table
            d: int  # d: Number of hash functions
    ):
        self._m = m
        self._d = d
        self._edge_count: int = 0

        self._tables = np.zeros((d, m))  # d rows ; m cols

    def add_edge(self, x: str):
        new_buckets_occupied = 0

        for i, x_hash in zip(range(self._d), self._hash(x)):
            if self._tables[i][x_hash] == 0:
                new_buckets_occupied += 1
            self._tables[i][x_hash] += 1
        self._edge_count += 1

        return new_buckets_occupied

    def get_edge_frequency(self, x: str):
        return min([self._tables[i][x_hash] for i, x_hash in zip(range(self._d), self._hash(x))])

    def _hash(self, x: str):
        x_hash = hashlib.md5(str(hash(x)).encode('utf-8'))
        for i in range(self._d):
            x_hash.update(str(i).encode('utf-8'))
            yield int(x_hash.hexdigest(), 16) % self._m


class CountMin(Sketch):
    name = Sketches.countmin.name

    def __init__(
            self,
            # [INT_SIZE * m * d]
            # [2 bytes * (1024 * 32) * 8 = 512 KB]
            m: int,  # m: Size of the hash table
            d: int  # d: Number of hash functions
    ):
        self._m = m
        self._d = d

        self._table = None

    @timeit
    def initialize(self):
        self.total_buckets = self._m * self._d
        self.used_buckets = 0

        self._table = CountMinTable(self._m, self._d)

    def add_edge(self, source_id, target_id):
        new_buckets_occupied = self._table.add_edge('{},{}'.format(source_id, target_id))
        self.used_buckets += new_buckets_occupied

    def get_edge_frequency(self, source_id, target_id):
        return self._table.get_edge_frequency('{},{}'.format(source_id, target_id))

    @timeit
    def print_analytics(self):
        print('Bucket ratio (used/total) : {:,}/{:,} ({}%)'.format(self.used_buckets, self.total_buckets, self.used_buckets / self.total_buckets * 100.0))

        # return {
        #     'edge_count': self._table._edge_count,
        #     'table_object_size': asizeof.asizeof(self._table._tables)
        # }
