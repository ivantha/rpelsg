from common.utils import timeit
from sketches import Sketches
from sketches.sketch import Sketch


class Beta(Sketch):
    name = Sketches.beta.name

    def __init__(self):
        pass

    @timeit
    def initialize(self):
        pass

    def add_edge(self, source_id, target_id):
        pass

    def get_edge_frequency(self, source_id, target_id):
        pass

    @timeit
    def print_analytics(self):
        pass
