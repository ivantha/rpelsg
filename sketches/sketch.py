from abc import ABC, abstractmethod
from typing import Callable

from common import utils


class Sketch(ABC):

    def __init__(self, base_path: str, streaming_path: str):
        """
        :param base_path: Path of the sample vertices list that will be used to create the base graph
        :param streaming_path: Path of the vertices list that will be streamed
        """
        self.base_path = base_path
        self.streaming_path = streaming_path

    @abstractmethod
    def construct_base_graph(self):
        pass

    @abstractmethod
    def construct_stream_graph(self):
        pass

    @abstractmethod
    def print_analytics(self, file):
        pass

    @staticmethod
    def _stream(path: str, edge_fun: Callable[[str, str], None]):
        data_files = utils.get_txt_files(path)
        for data_file in data_files:
            for line in utils.get_lines(data_file):
                source_id, target_id = line.strip().split(',')
                edge_fun(source_id, target_id)