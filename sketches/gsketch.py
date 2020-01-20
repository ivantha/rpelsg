import operator
from typing import List

from pympler import asizeof

from common import sampling
from common.utils import timeit
from sketches import Sketches
from sketches.countmin import CountMinTable
from sketches.sketch import Sketch


class SketchHash:
    def __init__(self):
        self.countmin_tables = []
        self.hash = {}

        self.outliers = None


class BptNode:
    def __init__(self, vertices: [], width: int):
        # Sketch properties
        self.vertices = vertices  # Sorted in ASC of f_v(m) / d_(m)
        self.width = width


class BinaryPartitionTree:
    def __init__(
            self,
            sample_stream: [(str, str)],
            sketch_total_width: int,
            sketch_depth: int,
            w_0: int,
            C: float
    ):
        # initial parameters
        self.sample_stream = sample_stream
        self.sketch_total_width = sketch_total_width
        self.sketch_depth = sketch_depth
        self.w_0 = w_0
        self.C = C

        self.root = None  # Root node
        self.sketch_hash = SketchHash()  # Hash-structure for edge-sketch in a dictionary

        # vertex properties
        self.vertices = set()
        self.vertex_relative_frequency = {}
        self.vertex_out_degree = {}
        self.vertex_average_frequency = {}  # f_v(m) / d_(m)

    def partition(self):
        # Calculate edges, vertices, vertex frequencies => O(n)
        temp_out_degree_set = {}
        for i, j in self.sample_stream:
            # Add to vertices
            self.vertices.add(i)
            self.vertices.add(j)

            # Add to vertex relative frequencies in i
            self.vertex_relative_frequency[i] = self.vertex_relative_frequency.get(i, 0) + 1

            #TODO
            # self.vertex_relative_frequency[j] = self.vertex_relative_frequency.get(j, 0) + 1

            # keep track of vertices
            if i not in temp_out_degree_set:
                temp_out_degree_set[i] = set()
            temp_out_degree_set[i].add(j)

            #TODO
            # if j not in temp_out_degree_set:
            #     temp_out_degree_set[j] = set()
            # temp_out_degree_set[j].add(i)

        # Calculate out degrees
        for v in temp_out_degree_set.keys():
            # Add to vertex out degrees in i
            self.vertex_out_degree[v] = len(temp_out_degree_set[v])

        # Set vertices without relative frequency & out degree count to 0 instead of None to stop NoneType errors
        for vertex in self.vertices:
            if vertex not in self.vertex_relative_frequency:
                self.vertex_relative_frequency[vertex] = 0
            if vertex not in self.vertex_out_degree:
                self.vertex_out_degree[vertex] = 0

        # Calculate average frequencies => O(n)
        for vertex in self.vertices:
            if self.vertex_relative_frequency[vertex] == 0:
                self.vertex_average_frequency[vertex] = 0
            else:
                self.vertex_average_frequency[vertex] = self.vertex_relative_frequency[vertex] / self.vertex_out_degree[vertex]

        # Sort the vertices by average frequency (Timesort) => O(n log n)
        sorted_vertices = sorted(self.vertex_average_frequency.items(), key=operator.itemgetter(1))
        sorted_vertices = [vertex for (vertex, average_frequency) in sorted_vertices]

        # Create a root node => O(1)
        self.root = BptNode(sorted_vertices, self.sketch_total_width)

        # Push the root node to the stack => O(1)
        stack = [self.root]

        # Loop while stack is not empty => O(w / w_0 - 1) According to the paper gSketch
        while len(stack) is not 0:
            current_sketch = stack.pop()

            print('part : {}'.format(current_sketch.width))

            # Calculate distinct edges
            distinct_edge_count = 0
            for vertex in current_sketch.vertices:  # => O(n)
                distinct_edge_count += self.vertex_out_degree[vertex]

            c1 = current_sketch.width < self.w_0  # Terminating condition 1
            c2 = distinct_edge_count <= self.C * current_sketch.width  # Terminating condition 2

            if c1:
                print('c1 : width - {}'.format(current_sketch.width))
            elif c2:
                print('c2 : # distinct edges - {} : width - {}'.format(distinct_edge_count, current_sketch.width))

            if c1 or c2 or len(current_sketch.vertices) == 1:  # Enough partitioning
                # Append the current sketch to the list of sketches => O(1)
                table = CountMinTable(current_sketch.width, self.sketch_depth)
                self.sketch_hash.countmin_tables.append(table)

                # Save index of leaf(sketch) at leaves in sketch_hash => O(n)
                idx = len(self.sketch_hash.countmin_tables) - 1
                for vertex in current_sketch.vertices:
                    self.sketch_hash.hash[vertex] = idx
            else:  # Partition some more
                # Calculate E
                def calculate_E(vertices, pivot):
                    # Calculate F_S1
                    F_S1 = sum([self.vertex_relative_frequency[vertices[i]] for i in range(0, pivot)])

                    # Calculate E1
                    E1 = 0
                    for i in range(0, pivot):
                        if self.vertex_out_degree[vertices[i]] != 0:
                            E1 += ((self.vertex_out_degree[vertices[i]] * F_S1) / self.vertex_average_frequency[vertices[i]])
                        else:
                            # TODO
                            if self.vertex_average_frequency[vertices[i]] != 0:
                                print('A very filthy exit! Gotta find out why this happened!!')
                                exit(-4)

                    # Calculate F_S2
                    F_S2 = sum([self.vertex_relative_frequency[vertices[i]] for i in range(pivot, len(vertices))])

                    # Calculate E1
                    E2 = 0
                    for i in range(pivot, len(vertices)):
                        if self.vertex_out_degree[vertices[i]] != 0:
                            E2 += ((self.vertex_out_degree[vertices[i]] * F_S2) / self.vertex_average_frequency[vertices[i]])
                        else:
                            # TODO
                            if self.vertex_average_frequency[vertices[i]] != 0:
                                print('A very filthy exit! Gotta find out why this happened!!')
                                exit(-4)

                    E = E1 + E2

                    return E

                E_values = [calculate_E(current_sketch.vertices, i) for i in range(1, len(current_sketch.vertices))]
                min_E_pivot = E_values.index(min(E_values)) + 1
                print('{}====={}'.format(len(E_values), min_E_pivot))

                # Create two new partition nodes
                stack.append(BptNode(current_sketch.vertices[:min_E_pivot:], int(current_sketch.width / 2)))
                stack.append(BptNode(current_sketch.vertices[min_E_pivot::], int(current_sketch.width / 2)))


class GSketch(Sketch):
    name = Sketches.gsketch.name

    def __init__(
            self,
            base_edges: List,

            # total sketch => [2 bytes * (1024 * 32) * 8 = 512 KB]
            w: int = 1024 * 32,  # m: Total width of the hash table (➡️)
            d: int = 8,  # d: Number of hash functions (⬇️)

            sample_size: int = 20000,
            w_0: int = 100,
            C: float = 1.0
    ):
        self.base_edges = base_edges

        self.w = w  # sketch width
        self.d = d  # sketch depth

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
        self.bpt = BinaryPartitionTree(self.sample_stream, round(self.w * 0.9), self.d, self.w_0, self.C)
        self.bpt.partition()

        # create outlier sketch
        self.bpt.sketch_hash.outliers = CountMinTable(round(self.w * 0.1), self.d)

        self.partitioned_edges = 0
        self.outlier_edges = 0

    def add_edge(self, source_id, target_id):
        if source_id in self.bpt.sketch_hash.hash:
            self.bpt.sketch_hash.countmin_tables[self.bpt.sketch_hash.hash[source_id]].add_edge('{},{}'.format(source_id, target_id))
            self.partitioned_edges += 1
        else:
            self.bpt.sketch_hash.outliers.add_edge('{},{}'.format(source_id, target_id))
            self.outlier_edges += 1

    def get_edge_frequency(self, source_id, target_id):
        if source_id in self.bpt.sketch_hash.hash:
            return self.bpt.sketch_hash.countmin_tables[self.bpt.sketch_hash.hash[source_id]]\
                .get_edge_frequency('{},{}'.format(source_id, target_id))
        else:
            return self.bpt.sketch_hash.outliers\
                .get_edge_frequency('{},{}'.format(source_id, target_id))

    @timeit
    def print_analytics(self):
        print('# partitions: {}'.format(len(self.bpt.sketch_hash.countmin_tables)))
        print('# partitioned edges : {}'.format(self.partitioned_edges))
        print('# outlier edges : {}'.format(self.outlier_edges))

        # return {
        #     'sketch_hash_object_size': asizeof.asizeof(self.bpt.sketch_hash)
        # }
