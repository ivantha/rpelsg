# Edge weight distribution

import gc
import json
import os

from common import utils
from sketches.alpha import Alpha
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gmatrix import GMatrix
from sketches.gsketch import GSketch
from sketches.tcm import TCM
from tests.memory_profile import MemoryProfile


def ewd_test(datasets):
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
