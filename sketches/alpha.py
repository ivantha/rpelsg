import math
import operator
from typing import List

from pympler import asizeof

from common import sampling
from common.utils import timeit
from sketches import Sketches
from sketches.sketch import Sketch
from sketches.tcm import TcmTable


class SketchHash:
    def __init__(self):
        self.tcm_tables = []
        self.hash = {}

        self.outliers = None


class BptNode:
    def __init__(self, vertices: [], width: int):
        # self.left = None
        # self.right = None

        # Sketch properties
        self.vertices = vertices  # Sorted in ASC of f_v(m) / d_(m)
        self.width = width


class BinaryPartitionTree:
    def __init__(
            self,
            sample_stream: [(str, str)],
            total_sketch_width,
            sketch_depth,
            w_0: int,
            C: int
    ):
        # initial parameters
        self.sample_stream = sample_stream
        self.total_sketch_width = total_sketch_width
        self.sketch_depth = sketch_depth
        self.w_0 = w_0
        self.C = C

        self.root = None  # Root node
        self.sketch_hash = SketchHash()  # Hash-structure for edge-sketch in a dictionary

        # vertex properties
        self.vertices = []
        self.vertex_relative_frequency = {}
        self.vertex_out_degree = {}
        self.vertex_average_frequency = {}  # f_v(m) / d_(m)

        # sketch sizes
        total_sketch_size = 2 * total_sketch_width * total_sketch_width * self.sketch_depth / 1024.0
        self.partitioned_sketch_size = 0
        self.outlier_sketch_size = total_sketch_size * 0.25  # initial + remaining sketch size after partitioning => root(x) = outlier_sketch_width

        initial_partitioned_sketch_size = total_sketch_size * 0.75  # but the total assigned width won't be used!!
        self.partitionable_width = round(math.sqrt(initial_partitioned_sketch_size * 1024.0 / 2.0 / self.sketch_depth))

    def partition(self):
        # Calculate edges, vertices, vertex frequencies and out degrees => O(n)
        for i, j in self.sample_stream:
            # Add to vertices
            self.vertices.append(i)
            self.vertices.append(j)

            # Add to vertex frequencies in i,j
            self.vertex_relative_frequency[i] = self.vertex_relative_frequency.get(i, 0) + 1
            self.vertex_relative_frequency[j] = self.vertex_relative_frequency.get(j, 0) + 1

            # Add to vertex out degrees in i
            self.vertex_out_degree[i] = self.vertex_out_degree.get(i, 0) + 1

        # TODO : What do we do when out degree is zero?
        # Set vertices without out degree count to 1 instead of None to stop NoneType errors
        for vertex in self.vertices:
            if vertex not in self.vertex_out_degree:
                self.vertex_out_degree[vertex] = 1

        # Calculate average frequencies => O(n)
        for vertex in self.vertices:
            if self.vertex_out_degree.get(vertex) == 0:
                self.vertex_average_frequency[vertex] = 0
            else:
                self.vertex_average_frequency[vertex] = self.vertex_relative_frequency.get(
                    vertex) / self.vertex_out_degree.get(vertex)

        # Sort the vertices by average frequency => O(n log n)
        # TODO : Use quick-sort (or something known) instead of Python sort
        sorted_vertices = sorted(self.vertex_average_frequency.items(), key=operator.itemgetter(1))
        sorted_vertices = [vertex for (vertex, average_frequency) in sorted_vertices]

        # Create a root node => O(1)
        self.root = BptNode(sorted_vertices, self.partitionable_width)

        # Push the root node to the stack => O(1)
        stack = [self.root]

        # Loop while stack is not empty => O(w / w_0 - 1) According to the paper gSketch
        while len(stack) is not 0:
            current_sketch = stack.pop()

            # Calculate distinct edges
            distinct_edge_count = 0
            for vertex in current_sketch.vertices:  # => O(n)
                distinct_edge_count += self.vertex_out_degree.get(vertex)

            c1 = current_sketch.width < self.w_0  # Terminating condition 1
            c2 = distinct_edge_count <= self.C * current_sketch.width  # Terminating condition 2

            if c1 or c2:  # Enough partitioning
                # Append the current sketch to the list of sketches => O(1)
                table = TcmTable(current_sketch.width, self.sketch_depth)
                self.sketch_hash.tcm_tables.append(table)

                # Save index of leaf(sketch) at leaves in sketch_hash => O(n)
                idx = len(self.sketch_hash.tcm_tables) - 1
                for vertex in current_sketch.vertices:
                    self.sketch_hash.hash[vertex] = idx

                # report: partitioned size
                self.partitioned_sketch_size += (2 * current_sketch.width * current_sketch.width * self.sketch_depth / 1024.0)
            else:  # Partition some more
                # Calculate E
                def calculate_E(vertices, pivot):
                    # Calculate F_S1
                    F_S1 = 0
                    for i in range(0, pivot):
                        F_S1 += self.vertex_relative_frequency.get(vertices[i])

                    # Calculate F_S2
                    F_S2 = 0
                    for i in range(pivot, len(vertices)):
                        F_S2 += self.vertex_relative_frequency.get(vertices[i])

                    # Calculate E1
                    E1 = 0
                    for i in range(0, pivot):
                        E1 += ((self.vertex_out_degree.get(vertices[i]) * F_S1) / self.vertex_average_frequency.get(
                            vertices[i]))

                    # Calculate E1
                    E2 = 0
                    for i in range(pivot, len(vertices)):
                        E2 += ((self.vertex_out_degree.get(vertices[i]) * F_S1) / self.vertex_average_frequency.get(
                            vertices[i]))

                    E = E1 + E2

                    return E

                min_E = (1, calculate_E(current_sketch.vertices, 1))  # (partition_index, min_value)
                for i in range(2, len(current_sketch.vertices)):  # => O(n) This probably gets reduced over iterations
                    E_val = calculate_E(current_sketch.vertices, i)
                    if E_val < min_E[1]:
                        min_E = [i, E_val]

                # Create two new partition nodes
                stack.append(BptNode(current_sketch.vertices[:min_E[0]], int(current_sketch.width / 2)))
                stack.append(BptNode(current_sketch.vertices[min_E[0]:], int(current_sketch.width / 2)))

                # add to outlier (remaining) sketch size
                x = current_sketch.width / 2.0
                rem_quarter = 2.0 * x * x * self.sketch_depth / 1024.0
                self.outlier_sketch_size += (2 * rem_quarter)


class Alpha(Sketch):
    name = Sketches.alpha.name

    def __init__(
            self,
            base_edges: List,
            streaming_edges: List,

            # total sketch => [2 bytes * (181 * 181) * 8 = 511.9 KB)]
            total_sketch_width: int = 181,  # m: Total width of the hash table (➡️)

            sketch_depth: int = 8,  # d: Number of hash functions (⬇️)

            sample_size: int = 10000,
            w_0: int = 200,
            C: int = 10
    ):
        self.base_edges = base_edges
        self.streaming_edges = streaming_edges

        self.total_sketch_width = total_sketch_width
        self.sketch_depth = sketch_depth

        self.sample_size = sample_size
        self.w_0 = w_0
        self.C = C

        self.sample_stream = None
        self.bpt = None

    @timeit
    def initialize(self):
        # reservoir sampling for k items as (i, j)
        self.sample_stream = sampling.select_k_items(self.base_edges, self.sample_size)

        # partition sketches
        self.bpt = BinaryPartitionTree(self.sample_stream, self.total_sketch_width, self.sketch_depth, self.w_0, self.C)
        self.bpt.partition()

        # create outlier sketch
        outlier_sketch_width = round(math.sqrt(self.bpt.outlier_sketch_size * 1024.0 / 2.0 / self.sketch_depth))
        self.bpt.sketch_hash.outliers = TcmTable(outlier_sketch_width, self.sketch_depth)

        print('{}KB (Partitioned) : {}KB (Outlier)'.format(self.bpt.partitioned_sketch_size, self.bpt.outlier_sketch_size))
        print('Outlier sketch width: {}'.format(outlier_sketch_width))
        print('# partitions: {}'.format(len(self.bpt.sketch_hash.tcm_tables)))

    def add_edge(self, source_id, target_id):
        if source_id in self.bpt.sketch_hash.hash:
            self.bpt.sketch_hash.tcm_tables[self.bpt.sketch_hash.hash.get(source_id)].add_edge(source_id, target_id)
        else:
            self.bpt.sketch_hash.outliers.add_edge(source_id, target_id)

    def get_edge_frequency(self, source_id, target_id):
        if source_id in self.bpt.sketch_hash.hash:
            return self.bpt.sketch_hash.tcm_tables[self.bpt.sketch_hash.hash.get(source_id)]\
                .get_edge_frequency(source_id, target_id)
        else:
            return self.bpt.sketch_hash.outliers\
                .get_edge_frequency(source_id, target_id)

    @timeit
    def get_analytics(self):
        return {
            'sketch_hash_object_size': asizeof.asizeof(self.bpt.sketch_hash)
        }
