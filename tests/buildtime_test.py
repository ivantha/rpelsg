import gc
import json
import os
from datetime import datetime as dtt

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from common import utils
from sketches import Sketches
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gmatrix import GMatrix
from sketches.gsketch import GSketch
from sketches.kmatrix import KMatrix
from sketches.tcm import TCM
from tests.memory_profile import MemoryProfile


def test(datasets):
    print(os.path.basename(__file__).split('.')[0])

    edge_lists = []
    for dataset in datasets:
        edge_lists.append(utils.get_edges_in_path(dataset))

    memory_profiles = (
        (MemoryProfile.fullgraph, FullGraph()),  # 512 KB

        # (MemoryProfile.countmin_100, CountMin(m=1024 * 7, d=7)),
        # (MemoryProfile.countmin_200, CountMin(m=1024 * 14, d=7)),
        # (MemoryProfile.countmin_300, CountMin(m=1024 * 21, d=7)),
        # (MemoryProfile.countmin_400, CountMin(m=1024 * 29, d=7)),
        # (MemoryProfile.countmin_512, CountMin(m=1024 * 37, d=7)),
        (MemoryProfile.countmin_1024, CountMin(m=1024 * 73, d=7)),
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
        (MemoryProfile.gsketch_1024, GSketch(edge_lists, w=1024 * 73, d=7)),
        # (MemoryProfile.gsketch_2048, GSketch(edge_lists, w=1024 * 146, d=7)),
        # (MemoryProfile.gsketch_4096, GSketch(edge_lists, w=1024 * 293, d=7)),
        # (MemoryProfile.gsketch_8192, GSketch(edge_lists, w=1024 * 585, d=7)),
        # (MemoryProfile.gsketch_16384, GSketch(edge_lists, w=1024 * 1170, d=7)),
        # (MemoryProfile.gsketch_32768, GSketch(edge_lists, w=1024 * 2341, d=7)),
        # (MemoryProfile.gsketch_65536, GSketch(edge_lists, w=1024 * 4681, d=7)),

        # (MemoryProfile.tcm_100, TCM(w=86, d=7)),
        # (MemoryProfile.tcm_200, TCM(w=121, d=7)),
        # (MemoryProfile.tcm_300, TCM(w=148, d=7)),
        # (MemoryProfile.tcm_400, TCM(w=171, d=7)),
        # (MemoryProfile.tcm_512, TCM(w=194, d=7)),
        (MemoryProfile.tcm_1024, TCM(w=274, d=7)),
        # (MemoryProfile.tcm_2048, TCM(w=387, d=7)),
        # (MemoryProfile.tcm_4096, TCM(w=547, d=7)),
        # (MemoryProfile.tcm_8192, TCM(w=774, d=7)),
        # (MemoryProfile.tcm_16384, TCM(w=1095, d=7)),
        # (MemoryProfile.tcm_32768, TCM(w=1548, d=7)),
        # (MemoryProfile.tcm_65536, TCM(w=2189, d=7)),

        # (MemoryProfile.gmatrix_100, GMatrix(w=86, d=7)),
        # (MemoryProfile.gmatrix_200, GMatrix(w=121, d=7)),
        # (MemoryProfile.gmatrix_300, GMatrix(w=148, d=7)),
        # (MemoryProfile.gmatrix_400, GMatrix(w=171, d=7)),
        # (MemoryProfile.gmatrix_512, GMatrix(w=194, d=7)),
        (MemoryProfile.gmatrix_1024, GMatrix(w=274, d=7)),
        # (MemoryProfile.gmatrix_2048, GMatrix(w=387, d=7)),
        # (MemoryProfile.gmatrix_4096, GMatrix(w=547, d=7)),
        # (MemoryProfile.gmatrix_8192, GMatrix(w=774, d=7)),
        # (MemoryProfile.gmatrix_16384, GMatrix(w=1095, d=7)),
        # (MemoryProfile.gmatrix_32768, GMatrix(w=1548, d=7)),
        # (MemoryProfile.gmatrix_65536, GMatrix(w=2189, d=7)),

        # (MemoryProfile.kmatrix_100, KMatrix(edge_lists, w=86, d=7)),
        # (MemoryProfile.kmatrix_200, KMatrix(edge_lists, w=121, d=7)),
        # (MemoryProfile.kmatrix_300, KMatrix(edge_lists, w=148, d=7)),
        # (MemoryProfile.kmatrix_400, KMatrix(edge_lists, w=171, d=7)),
        # (MemoryProfile.kmatrix_512, KMatrix(edge_lists, w=194, d=7)),
        (MemoryProfile.kmatrix_1024, KMatrix(edge_lists, w=274, d=7)),
        # (MemoryProfile.kmatrix_2048, KMatrix(edge_lists, w=387, d=7)),
        # (MemoryProfile.kmatrix_4096, KMatrix(edge_lists, w=547, d=7)),
        # (MemoryProfile.kmatrix_8192, KMatrix(edge_lists, w=774, d=7)),
        # (MemoryProfile.kmatrix_16384, KMatrix(edge_lists, w=1095, d=7)),
        # (MemoryProfile.kmatrix_32768, KMatrix(edge_lists, w=1548, d=7)),
        # (MemoryProfile.kmatrix_65536, KMatrix(edge_lists, w=2189, d=7)),
    )

    test_output_dir = '../output/{}'.format(os.path.basename(__file__).split('.')[0])
    os.makedirs(test_output_dir, exist_ok=True)

    for sketch_id, sketch in memory_profiles:
        initialize_start_time, initialize_end_time = sketch.initialize()  # initialize the sketch

        # stream edges
        streaming_times = []
        for edge_list in edge_lists:
            streaming_times.append(sketch.stream(edge_list))

        streaming_start_time = streaming_times[0][0]
        streaming_end_time = streaming_times[-1][1]

        # set time info
        sketch.initialize_time = initialize_end_time - initialize_start_time
        sketch.streaming_time = streaming_end_time - streaming_start_time

        output = {
            'sketch_id': sketch_id.name,
            'sketch': sketch.name,
            'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
            'initialize_time': '{}'.format(sketch.initialize_time),
            'streaming_time': '{}'.format(sketch.streaming_time),
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
    print(os.path.basename(__file__).split('.')[0])

    sketches = (
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.gmatrix.name, 'gMatrix'),
        (Sketches.kmatrix.name, 'kMatrix'),
    )

    sketch_sizes = (
        # (100, '100 KB'),
        # (200, '200 KB'),
        # (300, '300 KB'),
        # (400, '400 KB'),
        # (512, '512 KB'),
        (1024, '1 MB'),
        # (2048, '2 MB'),
        # (4096, '4 MB'),
        # (8192, '8 MB'),
        # (16384, '16 MB'),
        # (32768, '32 MB'),
        # (65536, '64 MB')
    )

    test_output_dir = '../output/{}'.format(os.path.basename(__file__).split('.')[0])

    for sketch_size, pretty_size in sketch_sizes:
        results = []

        for sketch_name, pretty_name in sketches:
            with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                output = json.load(file)
                output['initialize_time'] = (
                        dtt.strptime(output['initialize_time'], '%H:%M:%S.%f') - dtt.strptime("00:00", "%H:%M")
                ).total_seconds()
                output['streaming_time'] = (
                        dtt.strptime(output['streaming_time'], '%H:%M:%S.%f') - dtt.strptime("00:00", "%H:%M")
                ).total_seconds()
                results.append(output)

        matplotlib.rcParams['figure.dpi'] = 500

        ind = np.arange(len(results))  # the x locations for the groups
        width = 0.35  # the width of the bars

        dataset = [
            [x['initialize_time'] for x in results],
            [x['streaming_time'] for x in results]
        ]

        fig = plt.figure()
        ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
        # ax.yaxis.grid(True)

        p1 = plt.bar(ind, dataset[0], width, color='none', edgecolor="#000000", hatch='\\\\')
        p2 = plt.bar(ind, dataset[1], width, bottom=dataset[0], color='none', edgecolor="#000000", hatch='.')

        plt.title('Sketch construction and streaming times : {}'.format(pretty_size))
        plt.ylabel('Time (s)')
        plt.xlabel('Sketches')
        plt.xticks(ind, [pretty_name for _, pretty_name in sketches])
        leg = plt.legend((p1[0], p2[0]), ('Initialization', 'Streaming'))

        fig.text(0.1, 0.06, '# edges : {:,}'.format(results[0]['edge_count']))

        test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
        os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
        plt.savefig('../reports/{}/{}_{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name,
                                                     sketch_size))

        # plt.show()
        plt.close()

        print('Completed visualization: {}'.format(sketch_size))


if __name__ == '__main__':
    test(['../datasets/unicorn-wget-benign-base/50.txt'])
    visualize()
