# Degree centrality

import gc
import json
import os

from common import utils
from sketches.alpha import Alpha
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM
from tests.memory_profile import MemoryProfile


def dc_test(datasets):
    print('dc_test')

    edge_lists = []
    for dataset in datasets:
        edge_lists.append(utils.get_edges_in_path(dataset))

    memory_profiles = (
        (MemoryProfile.fullgraph, FullGraph()),  # 512 KB

        (MemoryProfile.countmin_512, CountMin(m=1024 * 32, d=8)),  # 512 KB
        (MemoryProfile.countmin_1024, CountMin(m=1024 * 32 * 2, d=8)),  # 1 MB
        (MemoryProfile.countmin_2048, CountMin(m=1024 * 32 * 4, d=8)),  # 2 MB
        (MemoryProfile.countmin_4096, CountMin(m=1024 * 32 * 8, d=8)),  # 4 MB
        (MemoryProfile.countmin_8192, CountMin(m=1024 * 32 * 16, d=8)),  # 8 MB
        (MemoryProfile.countmin_16384, CountMin(m=1024 * 32 * 32, d=8)),  # 16 MB
        (MemoryProfile.countmin_32768, CountMin(m=1024 * 32 * 64, d=8)),  # 32 MB
        (MemoryProfile.countmin_65536, CountMin(m=1024 * 32 * 128, d=8)),  # 64 MB

        (MemoryProfile.gsketch_512, GSketch(edge_lists[0],
                                            partitioned_sketch_width=1024 * 24, outlier_sketch_width=1024 * 8,
                                            sketch_depth=8)),  # 512 KB
        (MemoryProfile.gsketch_1024, GSketch(edge_lists[0],
                                             partitioned_sketch_width=1024 * 24 * 2, outlier_sketch_width=1024 * 8 * 2,
                                             sketch_depth=8)),  # 1 MB
        (MemoryProfile.gsketch_2048, GSketch(edge_lists[0],
                                             partitioned_sketch_width=1024 * 24 * 4, outlier_sketch_width=1024 * 8 * 4,
                                             sketch_depth=8)),  # 2 MB
        (MemoryProfile.gsketch_4096, GSketch(edge_lists[0],
                                             partitioned_sketch_width=1024 * 24 * 8, outlier_sketch_width=1024 * 8 * 8,
                                             sketch_depth=8)),  # 4 MB
        (MemoryProfile.gsketch_8192, GSketch(edge_lists[0],
                                             partitioned_sketch_width=1024 * 24 * 16,
                                             outlier_sketch_width=1024 * 8 * 16,
                                             sketch_depth=8)),  # 8 MB
        (MemoryProfile.gsketch_16384, GSketch(edge_lists[0],
                                              partitioned_sketch_width=1024 * 24 * 32,
                                              outlier_sketch_width=1024 * 8 * 32,
                                              sketch_depth=8)),  # 16 MB
        (MemoryProfile.gsketch_32768, GSketch(edge_lists[0],
                                              partitioned_sketch_width=1024 * 24 * 64,
                                              outlier_sketch_width=1024 * 8 * 64,
                                              sketch_depth=8)),  # 32 MB
        (MemoryProfile.gsketch_65536, GSketch(edge_lists[0],
                                              partitioned_sketch_width=1024 * 24 * 128,
                                              outlier_sketch_width=1024 * 8 * 128,
                                              sketch_depth=8)),  # 64 MB

        (MemoryProfile.tcm_512, TCM(w=181, d=8)),  # 511.8 KB
        (MemoryProfile.tcm_1024, TCM(w=256, d=8)),  # 1 MB
        (MemoryProfile.tcm_2048, TCM(w=362, d=8)),  # 1.9996 MB
        (MemoryProfile.tcm_4096, TCM(w=512, d=8)),  # 4 MB
        (MemoryProfile.tcm_8192, TCM(w=724, d=8)),  # 7.9983 MB
        (MemoryProfile.tcm_16384, TCM(w=1024, d=8)),  # 16 MB
        (MemoryProfile.tcm_32768, TCM(w=1448, d=8)),  # 31.9932 MB
        (MemoryProfile.tcm_65536, TCM(w=2048, d=8)),  # 64 MB

        (MemoryProfile.alpha_512, Alpha(edge_lists[0], total_sketch_width=181, sketch_depth=8)),  # 512 KB
        (MemoryProfile.alpha_1024, Alpha(edge_lists[0], total_sketch_width=256, sketch_depth=8)),  # 1 MB
        (MemoryProfile.alpha_2048, Alpha(edge_lists[0], total_sketch_width=362, sketch_depth=8)),  # 2 MB
        (MemoryProfile.alpha_4096, Alpha(edge_lists[0], total_sketch_width=512, sketch_depth=8)),  # 4 MB
        (MemoryProfile.alpha_8192, Alpha(edge_lists[0], total_sketch_width=724, sketch_depth=8)),  # 8 MB
        (MemoryProfile.alpha_16384, Alpha(edge_lists[0], total_sketch_width=1024, sketch_depth=8)),  # 16 MB
        (MemoryProfile.alpha_32768, Alpha(edge_lists[0], total_sketch_width=1448, sketch_depth=8)),  # 32 MB
        (MemoryProfile.alpha_65536, Alpha(edge_lists[0], total_sketch_width=2048, sketch_depth=8)),  # 64 MB
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

        degrees = {}

        # add all vertices
        for vertex in vertices:
            degrees[vertex] = 0

        for source_id, target_id in edges:
            f = sketch.get_edge_frequency(source_id, target_id)
            degrees[source_id] += f
            degrees[target_id] += f

        output = {
            'sketch_id': sketch_id.name,
            'sketch_name': sketch.name,
            'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
            'number_of_vertices': number_of_vertices,
            'degrees': degrees
        }

        with open('{}/{}.json'.format(test_output_dir, sketch_id.name), 'w') as file:
            json.dump(output, file, indent=4)

        print('Completed: {}'.format(sketch_id.name))

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
