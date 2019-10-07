from abc import ABC, abstractmethod


class Sketch(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def add_edge(self, source_id, target_id):
        pass

    @abstractmethod
    def print_analytics(self, file):
        pass
