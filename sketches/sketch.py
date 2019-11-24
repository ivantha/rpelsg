from abc import ABC, abstractmethod
import multiprocessing as mp
from pathos.multiprocessing import ProcessingPool as Pool

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

    # used by the pool for parallel processing
    def _add_edge(self, ids):
        self.add_edge(ids[0], ids[1])

    @abstractmethod
    def get_edge_frequency(self, source_id, target_id):
        pass

    @abstractmethod
    def get_analytics(self):
        pass

    @timeit
    def stream(self, path: str):
        pool = Pool(mp.cpu_count())  # process pool
        total_file_count = len(utils.get_txt_files(path))

        def stream_edge(line):
            source_id, target_id = line.strip().split(',')
            self.add_edge(source_id, target_id)

        for i, data_file in enumerate(utils.get_txt_files(path)):
            with open(data_file) as file:
                # parallel edge streaming
                pool.map(stream_edge, file.readlines())

                # sequential edge streaming
                # for line in file.readlines():
                #     source_id, target_id = line.strip().split(',')
                #     self.add_edge(source_id, target_id)

            # update progress bar
            utils.print_progress_bar(i, total_file_count - 1, prefix='Progress:', suffix=self.__class__.__name__,
                                     length=50)

    @timeit
    def time_critical_stream(self, path: str):
        for i, data_file in enumerate(utils.get_txt_files(path)):
            with open(data_file) as file:
                for line in file.readlines():
                    source_id, target_id = line.strip().split(',')
                    self.add_edge(source_id, target_id)
