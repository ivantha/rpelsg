import math
import operator
from typing import List

from pympler import asizeof

from common import sampling
from common.globals import INT_SIZE
from common.utils import timeit
from sketches import Sketches
from sketches.sketch import Sketch
from sketches.tcm import TcmTable


class BptNode:
    def __init__(self,
                 vertices: [],
                 w: int
                 ):
        # Sketch properties
        self.vertices = vertices  # Sorted in ASC of f_v(m) / d_(m)
        self.w = w


class BinaryPartitionTree:
    def __init__(
            self,
            sample_stream: [(str, str)],
            w,
            d,
            w_0: int,
            C: float
    ):
        self.sample_stream = sample_stream

        # initial parameters
        self.w = w
        self.d = d
        self.w_0 = w_0
        self.C = C

        self.tcm_tables = []  # countmin tables
        self.vertex_hash = {}  # hash-structure for edge-sketch in a dictionary
        self.outlier_vertices = None  # outlier vertices

        # vertex properties
        self.vertices = set()
        self.rel_freq = {}  # relative frequency of vertices
        self.out_degree = {}  # out degree of vertices
        self.avg_freq = {}  # f_v(m) / d_(m)
        self.err_numerator = {}  # d_(m) * d_(m) / f_v(m)

        # for partitioning
        self.rem_size = INT_SIZE * self.w * self.w * self.d

    def partition(self):
        # Calculate stuff
        seen_edges = set()
        for i, j in self.sample_stream:
            # Add to vertices
            self.vertices.add(i)

            if (i, j) in seen_edges:
                self.rel_freq[i] += 1
            else:
                if i not in self.rel_freq:
                    self.rel_freq[i] = 1
                else:
                    self.rel_freq[i] += 1

                if i not in self.out_degree:
                    self.out_degree[i] = 1
                else:
                    self.out_degree[i] += 1

            # add the edge as seen
            seen_edges.add((i, j))

        # Calculate average frequencies => O(n)
        self.avg_freq = {v: self.rel_freq[v] / self.out_degree[v] for v in self.vertices}

        self.err_numerator = {v: self.out_degree[v] * self.out_degree[v] / self.rel_freq[v] for v in self.vertices}

        # Sort the vertices by average frequency (Timesort) => O(n log n)
        sorted_vertices = sorted(self.avg_freq.items(), key=lambda item: item[1])
        sorted_vertices = [vertex for (vertex, average_frequency) in sorted_vertices]

        # Create a root node => O(1)
        # Create the stack with the root node as the only element => O(1)
        stack = [BptNode(sorted_vertices, self.w)]

        # Loop while stack is not empty => O(w / w_0 - 1) According to the paper gSketch
        while len(stack) != 0:
            curr_sketch = stack.pop()  # current sketch

            sum_freq = sum([self.rel_freq[v] for v in curr_sketch.vertices])
            sum_out_degree = sum([self.out_degree[v] for v in curr_sketch.vertices])  # Calculate distinct edges
            sum_numerate = sum([self.err_numerator[v] for v in curr_sketch.vertices])
            # sum_denom = sum([self.out_degree[v] for v in self.vertices])
            sum_denom = 1

            # current error
            base = (sum_freq * sum_numerate) / curr_sketch.w / sum_denom

            # print('Partitioning : width - {}, # vertices - {}, # edges - {}'.format(curr_sketch.w, len(curr_sketch.vertices), sum_out_degree))

            c1 = curr_sketch.w < self.w_0  # Terminating condition 1
            c2 = sum_out_degree <= self.C * curr_sketch.w  # Terminating condition 2
            c3 = len(curr_sketch.vertices) == 1

            if c2 or c1 or c3:
                if c2:
                    # print('c2', end='')

                    ratio_width = self.C
                    sketch_d = 2

                    new_width = int(sum_out_degree / ratio_width)
                    if new_width == 0:
                        new_width = 1
                    table = TcmTable(new_width, sketch_d)  # create sketch

                    self.rem_size -= INT_SIZE * new_width * new_width * sketch_d  # subtract from remaining space for outliers

                    # print(' : width - {}, # distinct edges - {}'.format(new_width, sum_out_degree))
                elif c1:
                    # print('c1', end='')

                    ratio_width = self.C
                    sketch_d = 1

                    new_width = int(curr_sketch.w / ratio_width)
                    if new_width == 0:
                        new_width = 1
                    table = TcmTable(new_width, sketch_d)  # create sketch

                    self.rem_size -= INT_SIZE * new_width * new_width * sketch_d  # subtract from remaining space for outliers

                    # print(' : width - {}, # distinct edges - {}'.format(new_width, sum_out_degree))
                else:  # c3
                    # print('c3', end='')

                    table = TcmTable(curr_sketch.w, self.d)  # create sketch

                    self.rem_size -= INT_SIZE * curr_sketch.w * curr_sketch.w * self.d  # subtract from remaining space for outliers

                    # print(' : width - {}, # distinct edges - {}'.format(curr_sketch.w, sum_out_degree))

                # append the created hash to table list
                self.tcm_tables.append(table)

                # save index of leaf(sketch) at leaves in sketch_hash
                idx = len(self.tcm_tables) - 1
                for vertex in curr_sketch.vertices:
                    self.vertex_hash[vertex] = idx
            else:  # Partition some more
                sub_sum_freq_1 = 0
                sub_width_1 = int(curr_sketch.w / 2)
                sub_sum_numerate_1 = 0
                sub_sum_denom_1 = 0

                sub_sum_freq_2 = sum_freq
                sub_width_2 = int(curr_sketch.w / 2)
                sub_sum_numerate_2 = sum_numerate
                sub_sum_denom_2 = sum_denom

                min_index = None
                min_value = 999999999999999999999.0

                Eg_List = []

                for i in range(0, len(curr_sketch.vertices) - 1):
                    curr_vertex = curr_sketch.vertices[i]
                    sub_sum_freq_1 += self.rel_freq[curr_vertex]
                    sub_sum_numerate_1 += self.out_degree[curr_vertex] * self.out_degree[curr_vertex] / \
                                          self.rel_freq[curr_vertex]
                    # sub_sum_denom_1 += self.out_degree[curr_vertex]
                    sub_sum_denom_1 = 1

                    sub_base_1 = (sub_sum_freq_1 * sub_sum_numerate_1) / sub_width_1 / sub_sum_denom_1

                    sub_sum_freq_2 -= self.rel_freq[curr_vertex]
                    sub_sum_numerate_2 -= self.out_degree[curr_vertex] * self.out_degree[curr_vertex] / \
                                          self.rel_freq[curr_vertex]
                    # sub_sum_denom_2 -= self.out_degree[curr_vertex]
                    sub_sum_denom_2 = 1

                    sub_base_2 = (sub_sum_freq_2 * sub_sum_numerate_2) / sub_width_2 / sub_sum_denom_2

                    error_gain = sub_base_1 + sub_base_2 - base

                    Eg_List.append(error_gain)

                    if error_gain < min_value:
                        min_index = i
                        min_value = error_gain

                # print('{}<=>{} (base:{:.10f}, max:{:.10f}, min:{:.10f})'.format(len(curr_sketch.vertices), min_index, base, max(Eg_List), min_value))

                # Create two new partition nodes
                stack.append(BptNode(curr_sketch.vertices[:min_index + 1], sub_width_1))
                stack.append(BptNode(curr_sketch.vertices[min_index + 1:], sub_width_2))


class KMatrix(Sketch):
    name = Sketches.alpha.name

    def __init__(
            self,
            base_edges: List,

            # total sketch =>
            # [INT_SIZE * w * w * d]
            # [2 bytes * (181 * 181) * 8 = 511.9 KB)]
            w: int,  # w: Total width of the hash table (➡️)
            d: int,  # d: Number of hash functions (⬇️)

            sample_size: int = 30000,
            # unicorn-wget, cit-HepPh
            w_0: int = 29,
            C: float = 0.2
            # email-EuAll, gen-scale-free, gen-small-world
            # w_0: int = 113,
            # C: float = 0.5
    ):
        self.base_edges = base_edges

        self.w = w  # sketch width
        self.d = d  # sketch depth

        self.sample_size = sample_size
        self.w_0 = w_0
        self.C = C

        self.sample_stream = None
        self.bpt = None

        self.partitioned_edges = 0
        self.outlier_edges = 0

    @timeit
    def initialize(self):
        # reservoir sampling for k items as (i, j)
        base_edge_count = sum([len(x) for x in self.base_edges])
        if base_edge_count > self.sample_size:
            self.sample_stream = sampling.select_k_items_from_lists(self.base_edges, self.sample_size)
        else:
            self.sample_stream = sampling.select_k_items_from_lists(self.base_edges, int(base_edge_count * 0.1))
            print('{} items are not present in the original stream. Choosing {} items from {} instead'.format(self.sample_size, int(base_edge_count * 0.1), base_edge_count))

        # partition sketches
        self.bpt = BinaryPartitionTree(self.sample_stream, self.w, self.d, self.w_0, self.C)
        self.bpt.partition()

        # create outlier sketch
        print('Remaining size for outliers : {} ({}%)'.format(self.bpt.rem_size, self.bpt.rem_size / (INT_SIZE * self.w * self.w * self.d) * 100.0))
        outlier_width = round(math.sqrt(self.bpt.rem_size / INT_SIZE / self.d))
        if outlier_width == 0:
            print('Outlier width 0 -> 1')
            outlier_width = 1
        print('Outlier size : {:.2f}KB ({:.2f}%)'.format(INT_SIZE * outlier_width * outlier_width * self.d / 1024.0, (outlier_width * outlier_width) / (self.w * self.w) * 100.0))
        self.bpt.outlier_vertices = TcmTable(outlier_width, self.d)

    def add_edge(self, source_id, target_id):
        if source_id in self.bpt.vertex_hash:
            self.bpt.tcm_tables[self.bpt.vertex_hash.get(source_id)].add_edge(source_id, target_id)
            self.partitioned_edges += 1
        else:
            self.bpt.outlier_vertices.add_edge(source_id, target_id)
            self.outlier_edges += 1

    def get_edge_frequency(self, source_id, target_id):
        if source_id in self.bpt.vertex_hash:
            return self.bpt.tcm_tables[self.bpt.vertex_hash.get(source_id)].get_edge_frequency(source_id, target_id)
        else:
            return self.bpt.outlier_vertices.get_edge_frequency(source_id, target_id)

    @timeit
    def print_analytics(self):
        print('# partitions: {}'.format(len(self.bpt.tcm_tables)))
        print('# partitioned edges : {}'.format(self.partitioned_edges))
        print('# outlier edges : {}'.format(self.outlier_edges))

        # return {
        #     'sketch_hash_object_size': asizeof.asizeof(self.bpt.sketch_hash)
        # }
