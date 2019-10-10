import hashlib

import numpy as np
from pympler import asizeof

from common.utils import timeit
from sketches import Sketches
from sketches.sketch import Sketch


class CountMinTable:
    def __init__(
            self,
            m: int,  # m: Size of the hash table (➡️)
            d: int  # d: Number of hash functions (⬇️)
    ):
        self._m = m
        self._d = d
        self._edge_count: int = 0

        self._tables = np.zeros((d, m))  # d rows ; m cols

    def add_edge(self, x: str):
        for i, x_hash in zip(range(self._d), self._hash(x)):
            self._tables[i][x_hash] += 1
        self._edge_count += 1

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
            # [2 bytes * (1024 * 32) * 8 = 512 KB]
            m: int = 1024 * 32,  # m: Size of the hash table (➡️)
            d: int = 8  # d: Number of hash functions (⬇️)
    ):
        self._m = m
        self._d = d

        self._table = None

    @timeit
    def initialize(self):
        self._table = CountMinTable(self._m, self._d)

    def add_edge(self, source_id, target_id):
        self._table.add_edge('{},{}'.format(source_id, target_id))

    def get_edge_frequency(self, source_id, target_id):
        return self._table.get_edge_frequency('{},{}'.format(source_id, target_id))

    @timeit
    def get_analytics(self):
        return {
            'edge_count': self._table._edge_count,
            'table_object_size': asizeof.asizeof(self._table._tables)
        }
