import time
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
        total_file_count = len(utils.get_txt_files(path))

        # initial call to print 0% progress
        utils.print_progress_bar(0, total_file_count, prefix='Progress:', suffix=self.__class__.__name__, length=50)

        for i, data_file in enumerate(utils.get_txt_files(path)):
            with open(data_file) as file:
                for line in file.readlines():
                    source_id, target_id = line.strip().split(',')
                    self.add_edge(source_id, target_id)

            # update progress bar
            utils.print_progress_bar(i + 1, total_file_count, prefix='Progress:', suffix=self.__class__.__name__, length=50)

            time.sleep(0.1)

    @timeit
    def time_critical_stream(self, path: str):
        for i, data_file in enumerate(utils.get_txt_files(path)):
            with open(data_file) as file:
                for line in file.readlines():
                    source_id, target_id = line.strip().split(',')
                    self.add_edge(source_id, target_id)
