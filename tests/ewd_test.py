import gc
import json
import os

import matplotlib
import matplotlib.pyplot as plt

from common import utils
from sketches import Sketches
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gmatrix import GMatrix
from sketches.gsketch import GSketch
from sketches.kmatrix import Alpha
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

        # (MemoryProfile.alpha_100, Alpha(edge_lists, w=86, d=7)),
        # (MemoryProfile.alpha_200, Alpha(edge_lists, w=121, d=7)),
        # (MemoryProfile.alpha_300, Alpha(edge_lists, w=148, d=7)),
        # (MemoryProfile.alpha_400, Alpha(edge_lists, w=171, d=7)),
        # (MemoryProfile.alpha_512, Alpha(edge_lists, w=194, d=7)),
        (MemoryProfile.alpha_1024, Alpha(edge_lists, w=274, d=7)),
        # (MemoryProfile.alpha_2048, Alpha(edge_lists, w=387, d=7)),
        # (MemoryProfile.alpha_4096, Alpha(edge_lists, w=547, d=7)),
        # (MemoryProfile.alpha_8192, Alpha(edge_lists, w=774, d=7)),
        # (MemoryProfile.alpha_16384, Alpha(edge_lists, w=1095, d=7)),
        # (MemoryProfile.alpha_32768, Alpha(edge_lists, w=1548, d=7)),
        # (MemoryProfile.alpha_65536, Alpha(edge_lists, w=2189, d=7)),
    )

    vertices = set()
    edges = set()

    for edge_list in edge_lists:
        for edge in edge_list:
            vertices.add(edge[0])  # add source_id
            vertices.add(edge[1])  # add target_id
            edges.add(edge)

    number_of_vertices = len(vertices)
    number_of_edges = len(edges)

    test_output_dir = '../output/{}/'.format(os.path.basename(__file__).split('.')[0])
    os.makedirs(os.path.dirname(test_output_dir), exist_ok=True)

    for sketch_id, sketch in memory_profiles:
        # init sketch
        sketch.initialize()
        for edge_list in edge_lists:
            sketch.stream(edge_list)

        edge_weights = {}

        # add all edges
        for source_id, target_id in edges:
            edge_weights['{},{}'.format(source_id, target_id)] = 0

        i = 0
        chunk = number_of_edges / 100
        for source_id, target_id in edges:
            f = sketch.get_edge_frequency(source_id, target_id)
            edge_weights['{},{}'.format(source_id, target_id)] = f

            # update progress bar
            i += 1
            if i % chunk == 0:
                utils.print_progress_bar(i, number_of_edges - 1, prefix='Progress:', suffix=sketch.name, length=50)

        edge_weight_distribution = {}
        for edge_weight in edge_weights.values():
            if edge_weight not in edge_weight_distribution:
                edge_weight_distribution[edge_weight] = edge_weight
            else:
                edge_weight_distribution[edge_weight] += edge_weight

        output = {
            'sketch_id': sketch_id.name,
            'sketch_name': sketch.name,
            'number_of_edges': sum([len(edge_list) for edge_list in edge_lists]),
            'number_of_vertices': number_of_vertices,
            'edge_weights': edge_weights,
            'edge_weight_distribution': edge_weight_distribution
        }

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
        (Sketches.fullgraph.name, 'FullGraph'),
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.gmatrix.name, 'GMatrix'),
        (Sketches.alpha.name, 'Alpha'),
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

    matplotlib.rcParams['figure.dpi'] = 500

    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])

    for sketch_name, pretty_name in sketches:
        for sketch_size, pretty_size in sketch_sizes:
            if sketch_name == Sketches.fullgraph.name:
                if sketch_size == 1024:
                    file = open('{}/{}.json'.format(test_output_dir, Sketches.fullgraph.name))
                    sketch_size = ''
                else:
                    break
            else:
                file = open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size))

            output = json.load(file)
            edge_weight_distribution = output['edge_weight_distribution']

            fig = plt.figure()
            ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
            ax.set_xscale("log")

            X = [int(float(i)) for i in edge_weight_distribution.keys()]
            Y = [i / 1000000 for i in edge_weight_distribution.values()]
            plt.scatter(X, Y, marker='.', s=10)

            plt.title('Edge weight distribution of {}'.format(pretty_name))
            plt.ylabel('Distribution (10^6)')
            plt.xlabel('Edge weight')

            fig.text(0.5, 0.03, '# edges : {:,}'.format(output['number_of_edges']))
            fig.text(0.1, 0.03, '# vertices : {:,}'.format(output['number_of_vertices']))

            test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
            os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
            plt.savefig('../reports/{}/{}_{}.png'.format(test_name, sketch_name, sketch_size))

            # plt.show()
            plt.close()

            print('Completed visualization: {}_{}'.format(sketch_name, sketch_size))
