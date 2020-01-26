from typing import List

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
    def __init__(self, vertices: [], w: int):
        # Sketch properties
        self.vertices = vertices  # Sorted in ASC of f_v(m) / d_(m)
        self.w = w


class BinaryPartitionTree:
    def __init__(
            self,
            sample_stream: [(str, str)],
            sketch_total_width: int,
            d: int,
            w_0: int,
            C: float
    ):
        # initial parameters
        self.sample_stream = sample_stream
        self.sketch_total_width = sketch_total_width
        self.d = d
        self.w_0 = w_0
        self.C = C

        self.sketch_hash = SketchHash()  # Hash-structure for edge-sketch in a dictionary

        # vertex properties
        self.vertices = set()
        self.relative_frequency = {}  # relative frequency of vertices
        self.out_degree = {}  # out degree of vertices
        self.average_frequency = {}  # f_v(m) / d_(m)
        self.error_numerator = {}  # d_(m) * d_(m) / f_v(m)

    def partition(self):
        # Calculate stuff
        seen_edges = set()
        for i, j in self.sample_stream:
            # Add to vertices
            self.vertices.add(i)

            if (i,j) in seen_edges:
                self.relative_frequency[i] += 1
            else:
                if i not in self.relative_frequency:
                    self.relative_frequency[i] = 1
                else:
                    self.relative_frequency[i] += 1

                if i not in self.out_degree:
                    self.out_degree[i] = 1
                else:
                    self.out_degree[i] += 1

            # add the edge as seen
            seen_edges.add((i,j))

        # Calculate average frequencies => O(n)
        self.average_frequency = {v: self.relative_frequency[v] / self.out_degree[v] for v in self.vertices}

        self.error_numerator = {v: self.out_degree[v] * self.out_degree[v] / self.relative_frequency[v] for v in self.vertices}

        # Sort the vertices by average frequency (Timesort) => O(n log n)
        sorted_vertices = sorted(self.average_frequency.items(), key=lambda item: item[1])
        sorted_vertices = [vertex for (vertex, average_frequency) in sorted_vertices]

        # Create a root node => O(1)
        # Create the stack with the root node as the only element => O(1)
        stack = [BptNode(sorted_vertices, self.sketch_total_width)]

        # Loop while stack is not empty => O(w / w_0 - 1) According to the paper gSketch
        while len(stack) is not 0:
            current_sketch = stack.pop()

            # Calculate distinct edges
            distinct_edge_count = sum([self.out_degree[v] for v in current_sketch.vertices])

            print('Partitioning : width - {}, # vertices - {}, # edges - {}'.format(current_sketch.w, len(current_sketch.vertices), distinct_edge_count))

            c1 = current_sketch.w < self.w_0  # Terminating condition 1
            c2 = distinct_edge_count <= self.C * current_sketch.w  # Terminating condition 2

            if c1:
                print('c1 : width - {}'.format(current_sketch.w))
            elif c2:
                print('c2 : width - {}, # distinct edges - {}'.format(current_sketch.w, distinct_edge_count))

            if c1 or c2 or len(current_sketch.vertices) == 1:  # Enough partitioning
                # Append the current sketch to the list of sketches => O(1)
                table = CountMinTable(current_sketch.w, self.d)
                self.sketch_hash.countmin_tables.append(table)

                # Save index of leaf(sketch) at leaves in sketch_hash => O(n)
                idx = len(self.sketch_hash.countmin_tables) - 1
                for vertex in current_sketch.vertices:
                    self.sketch_hash.hash[vertex] = idx
            else:  # Partition some more
                # current error
                current_F = sum([self.relative_frequency[v] for v in current_sketch.vertices])
                current_E_part1 = sum([self.error_numerator[v] for v in current_sketch.vertices])
                current_E = current_E_part1 * current_F

                # Calculate E
                def calculate_E(vertices, pivot):
                    F_S1 = sum([self.relative_frequency[vertices[i]] for i in range(0, pivot)])
                    E1_part1 = sum([self.error_numerator[vertices[i]] for i in range(0, pivot)])
                    E1_part2 = sum([self.out_degree[vertices[i]] for i in range(0, pivot)])
                    E1 = E1_part1 * F_S1 / E1_part2

                    F_S2 = sum([self.relative_frequency[vertices[i]] for i in range(pivot, len(vertices))])
                    E2_part1 = sum([self.error_numerator[vertices[i]] for i in range(pivot, len(vertices))])
                    E2_part2 = sum([self.out_degree[vertices[i]] for i in range(pivot, len(vertices))])
                    E2 = E2_part1 * F_S2 / E2_part2

                    E = E1 + E2

                    return E

                E_values = [calculate_E(current_sketch.vertices, i) for i in range(1, len(current_sketch.vertices))]
                min_E_pivot = E_values.index(min(E_values))
                print('{}<=>{}'.format(len(E_values), min_E_pivot))

                # Create two new partition nodes
                stack.append(BptNode(current_sketch.vertices[:min_E_pivot:], round(current_sketch.w / 2)))
                stack.append(BptNode(current_sketch.vertices[min_E_pivot::], round(current_sketch.w / 2)))


class GSketch(Sketch):
    name = Sketches.gsketch.name

    def __init__(
            self,
            base_edges: List,

            # total sketch => [2 bytes * (1024 * 32) * 8 = 512 KB]
            w: int = 1024 * 32,  # m: Total width of the hash table (➡️)
            d: int = 8,  # d: Number of hash functions (⬇️)

            sample_size: int = 10000,
            w_0: int = 20,
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
        self.sample_stream = sampling.select_k_items_from_lists(self.base_edges, self.sample_size)

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
            return self.bpt.sketch_hash.countmin_tables[self.bpt.sketch_hash.hash[source_id]].get_edge_frequency('{},{}'.format(source_id, target_id))
        else:
            return self.bpt.sketch_hash.outliers.get_edge_frequency('{},{}'.format(source_id, target_id))

    @timeit
    def print_analytics(self):
        print('# partitions: {}'.format(len(self.bpt.sketch_hash.countmin_tables)))
        print('# partitioned edges : {}'.format(self.partitioned_edges))
        print('# outlier edges : {}'.format(self.outlier_edges))

        # return {
        #     'sketch_hash_object_size': asizeof.asizeof(self.bpt.sketch_hash)
        # }
