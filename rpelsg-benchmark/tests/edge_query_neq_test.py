import gc
import json
import os

import matplotlib
import matplotlib.pyplot as plt

from common import utils, sampling
from sketches import Sketches
from sketches.full_graph import FullGraph
from sketches.gmatrix import GMatrix
from sketches.kmatrix import KMatrix
from sketches.tcm import TCM
from tests.memory_profile import MemoryProfile

test_output_dir = '../output/{}'.format(os.path.basename(__file__).split('.')[0])


def test(datasets):
    edge_lists = []
    for dataset in datasets:
        edge_lists.append(utils.get_edges_in_path(dataset))

    memory_profiles = (
        # (MemoryProfile.countmin_100, CountMin(m=1024 * 7, d=7)),
        # (MemoryProfile.countmin_200, CountMin(m=1024 * 14, d=7)),
        # (MemoryProfile.countmin_300, CountMin(m=1024 * 21, d=7)),
        # (MemoryProfile.countmin_400, CountMin(m=1024 * 29, d=7)),
        # (MemoryProfile.countmin_512, CountMin(m=1024 * 37, d=7)),
        # (MemoryProfile.countmin_1024, CountMin(m=1024 * 73, d=7)),
        # (MemoryProfile.countmin_2048, CountMin(m=1024 * 146, d=7)),
        # (MemoryProfile.countmin_4096, CountMin(m=1024 * 293, d=7)),
        # (MemoryProfile.countmin_8192, CountMin(m=1024 * 585, d=7)),
        # (MemoryProfile.countmin_16384, CountMin(m=1024 * 1170, d=7)),
        # (MemoryProfile.countmin_32768, CountMin(m=1024 * 2341, d=7)),
        # (MemoryProfile.countmin_65536, CountMin(m=1024 * 4681, d=7)),

        # (MemoryProfile.gsketch_100, GSketch(edge_lists, w=1024 * 7, d=7)),
        # (MemoryProfile.gsketch_200, GSketch(edge_lists, w=1024 * 14, d=7)),
        # (MemoryProfile.gsketch_300, GSketch(edge_lists, w=1024 * 21, d=7)),
        # (MemoryProfile.gsketch_400, GSketch(edge_lists, w=1024 * 29, d=7)),
        # (MemoryProfile.gsketch_512, GSketch(edge_lists, w=1024 * 37, d=7)),
        # (MemoryProfile.gsketch_1024, GSketch(edge_lists, w=1024 * 73, d=7)),
        # (MemoryProfile.gsketch_2048, GSketch(edge_lists, w=1024 * 146, d=7)),
        # (MemoryProfile.gsketch_4096, GSketch(edge_lists, w=1024 * 293, d=7)),
        # (MemoryProfile.gsketch_8192, GSketch(edge_lists, w=1024 * 585, d=7)),
        # (MemoryProfile.gsketch_16384, GSketch(edge_lists, w=1024 * 1170, d=7)),
        # (MemoryProfile.gsketch_32768, GSketch(edge_lists, w=1024 * 2341, d=7)),
        # (MemoryProfile.gsketch_65536, GSketch(edge_lists, w=1024 * 4681, d=7)),

        (MemoryProfile.tcm_100, TCM(w=86, d=7)),
        (MemoryProfile.tcm_200, TCM(w=121, d=7)),
        (MemoryProfile.tcm_300, TCM(w=148, d=7)),
        (MemoryProfile.tcm_400, TCM(w=171, d=7)),
        (MemoryProfile.tcm_512, TCM(w=194, d=7)),
        # (MemoryProfile.tcm_1024, TCM(w=274, d=7)),
        # (MemoryProfile.tcm_2048, TCM(w=387, d=7)),
        # (MemoryProfile.tcm_4096, TCM(w=547, d=7)),
        # (MemoryProfile.tcm_8192, TCM(w=774, d=7)),
        # (MemoryProfile.tcm_16384, TCM(w=1095, d=7)),
        # (MemoryProfile.tcm_32768, TCM(w=1548, d=7)),
        # (MemoryProfile.tcm_65536, TCM(w=2189, d=7)),

        (MemoryProfile.gmatrix_100, GMatrix(w=86, d=7)),
        (MemoryProfile.gmatrix_200, GMatrix(w=121, d=7)),
        (MemoryProfile.gmatrix_300, GMatrix(w=148, d=7)),
        (MemoryProfile.gmatrix_400, GMatrix(w=171, d=7)),
        (MemoryProfile.gmatrix_512, GMatrix(w=194, d=7)),
        # (MemoryProfile.gmatrix_1024, GMatrix(w=274, d=7)),
        # (MemoryProfile.gmatrix_2048, GMatrix(w=387, d=7)),
        # (MemoryProfile.gmatrix_4096, GMatrix(w=547, d=7)),
        # (MemoryProfile.gmatrix_8192, GMatrix(w=774, d=7)),
        # (MemoryProfile.gmatrix_16384, GMatrix(w=1095, d=7)),
        # (MemoryProfile.gmatrix_32768, GMatrix(w=1548, d=7)),
        # (MemoryProfile.gmatrix_65536, GMatrix(w=2189, d=7)),

        (MemoryProfile.kmatrix_100, KMatrix(edge_lists, w=86, d=7)),
        (MemoryProfile.kmatrix_200, KMatrix(edge_lists, w=121, d=7)),
        (MemoryProfile.kmatrix_300, KMatrix(edge_lists, w=148, d=7)),
        (MemoryProfile.kmatrix_400, KMatrix(edge_lists, w=171, d=7)),
        (MemoryProfile.kmatrix_512, KMatrix(edge_lists, w=194, d=7)),
        # (MemoryProfile.kmatrix_1024, KMatrix(edge_lists, w=274, d=7)),
        # (MemoryProfile.kmatrix_2048, KMatrix(edge_lists, w=387, d=7)),
        # (MemoryProfile.kmatrix_4096, KMatrix(edge_lists, w=547, d=7)),
        # (MemoryProfile.kmatrix_8192, KMatrix(edge_lists, w=774, d=7)),
        # (MemoryProfile.kmatrix_16384, KMatrix(edge_lists, w=1095, d=7)),
        # (MemoryProfile.kmatrix_32768, KMatrix(edge_lists, w=1548, d=7)),
        # (MemoryProfile.kmatrix_65536, KMatrix(edge_lists, w=2189, d=7)),
    )

    os.makedirs(test_output_dir, exist_ok=True)

    # init fullgraph
    full_graph = FullGraph()
    full_graph.initialize()
    for edge_list in edge_lists:
        full_graph.stream(edge_list)

    # reservoir sampling for 10000 items as (i, j) => 10000 queries
    sample_size = 10000
    sample_stream = sampling.select_k_items_from_lists(edge_lists, sample_size)

    for sketch_id, sketch in memory_profiles:
        # init sketch
        sketch.initialize()
        for edge_list in edge_lists:
            sketch.stream(edge_list)

        # query
        effective_query_count = 0
        for source_id, target_id in sample_stream:
            true_frequency = full_graph.get_edge_frequency(source_id, target_id)
            estimated_frequency = sketch.get_edge_frequency(source_id, target_id)
            if estimated_frequency == true_frequency:
                effective_query_count += 1

        output = {
            'sketch_id': sketch_id.name,
            'sketch_name': sketch.name,
            'memory_allocation': int(sketch_id.name.split('_')[1]),
            'number_of_edges': sum([len(edge_list) for edge_list in edge_lists]),
            'number_of_queries': sample_size,
            'effective_query_count': effective_query_count,
            'effective_query_percent': effective_query_count / sample_size
        }

        sketch.print_analytics()

        with open('{}/{}.json'.format(test_output_dir, sketch_id.name), 'w') as file:
            json.dump(output, file, indent=4)

        print('Completed: {}'.format(sketch_id.name))

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()


def visualize():
    sketches = (
        # (Sketches.countmin.name, 'CountMin', [2, 2, 2, 2]),
        # (Sketches.gsketch.name, 'gSketch', [2, 2, 10, 2]),
        (Sketches.tcm.name, 'TCM', 's', 'blue'),
        (Sketches.gmatrix.name, 'gMatrix', 'o', 'red'),
        (Sketches.kmatrix.name, 'kMatrix', 'D', 'green'),
    )

    sketch_sizes = (
        # (100, '100'),  # KB
        (200, '200'),  # KB
        (300, '300'),  # KB
        (400, '400'),  # KB
        (512, '512'),  # KB
        # (1024, '1'),  # MB
        # (2048, '2'),  # MB
        # (4096, '4'),  # MB
        # (8192, '8'),  # MB
        # (16384, '16'),  # MB
        # (32768, '32'),  # MB
        # (65536, '64')  # MB
    )

    plt.rcParams['figure.dpi'] = 500
    plt.rcParams["font.size"] = 20

    fig = plt.figure()

    for sketch_name, pretty_name, marker, color in sketches:
        memory_allocation = []
        effective_query_count = []
        effective_query_percent = []

        for sketch_size, pretty_size in sketch_sizes:
            with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                output = json.load(file)
                memory_allocation.append(output['memory_allocation'])
                effective_query_count.append(output['effective_query_count'])
                effective_query_percent.append(output['effective_query_percent'])

        plt.plot(
            memory_allocation,
            effective_query_count,
            label=pretty_name,
            color=color,
            marker=marker,
            markerfacecolor='none',
            markersize=14
        )

    plt.ylabel('NEQ')
    plt.xlabel('Memory (KB)')
    plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes])
    plt.legend()

    test_name = os.path.basename(__file__).split('.')[0]
    os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
    plt.savefig('../reports/{}/neq.png'.format(test_name), bbox_inches='tight')

    # plt.show()
    plt.close()


if __name__ == '__main__':
    print(os.path.basename(__file__).split('.')[0])
    test(['../datasets/unicorn-wget-benign-base/10.txt'])
    visualize()