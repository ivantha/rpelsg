from abc import ABC, abstractmethod

from common import utils
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
    def stream(self, path: str):
        for data_file in utils.get_txt_files(path):
            with open(data_file) as file:
                for line in file.readlines():
                    source_id, target_id = line.strip().split(',')
                    self.add_edge(source_id, target_id)
