from abc import ABC, abstractmethod


class Sketch(ABC):

    def __init__(self, base_path: str, streaming_path: str):
        self._base_path = base_path
        self._streaming_path = streaming_path

    def construct_base_graph(self):
        return self._stream(self._base_path)

    def stream_edges(self):
        return self._stream(self._streaming_path)

    @abstractmethod
    def print_analytics(self):
        pass

    @abstractmethod
    def _stream(self, path: str):
        pass
