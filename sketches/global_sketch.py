import hashlib
from _datetime import datetime

import numpy as np
from pympler import asizeof

from .sketch import Sketch
from utils import get_txt_files, get_lines


class Table:

    def __init__(self, m: int, d: int):
        """
        :param m: Size of the hash tables
        :param d: Number of hash tables
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


class GlobalSketch(Sketch):

    def __init__(self, base_path: str, streaming_path: str, m: int = 1048576, d: int = 5):
        """
        :param base_path:
        :param streaming_path:
        :param m: Size of the hash tables
        :param d: Number of hash tables
        """
        super().__init__(base_path, streaming_path)

        self._table = Table(m, d)

    def print_analytics(self):
        start_time = datetime.now()

        print('Edge count: {:,}'.format(self._table._edge_count))
        print('Table object size: {} bytes ({:.4f} MB)'.format(asizeof.asizeof(self._table._tables),
                                                               asizeof.asizeof(self._table._tables) / 1024.0 / 1024.0))

        end_time = datetime.now()

        return start_time, end_time

    def _stream(self, path: str):
        start_time = datetime.now()

        data_files = get_txt_files(path)
        for data_file in data_files:
            for line in get_lines(data_file):
                source_id, target_id = line.split()
                self._table.add_edge('{},{}'.format(source_id, target_id))

        end_time = datetime.now()

        return start_time, end_time
