# Heavy nodes

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


def hn_test(datasets):
    print('hn_test')

    edge_lists = []
    for dataset in datasets:
        edge_lists.append(utils.get_edges_in_path(dataset))

    memory_profiles = (
        (MemoryProfile.fullgraph, FullGraph()),  # 512 KB

        (MemoryProfile.countmin_100, CountMin(m=1024 * 6, d=8)),  # 96 KB
        (MemoryProfile.countmin_200, CountMin(m=1024 * 13, d=8)),  # 208 KB
        (MemoryProfile.countmin_300, CountMin(m=1024 * 19, d=8)),  # 304 KB
        (MemoryProfile.countmin_400, CountMin(m=1024 * 25, d=8)),  # 400 KB
        (MemoryProfile.countmin_512, CountMin(m=1024 * 32, d=8)),  # 512 KB
        # (MemoryProfile.countmin_1024, CountMin(m=1024 * 32 * 2, d=8)),  # 1 MB
        # (MemoryProfile.countmin_2048, CountMin(m=1024 * 32 * 4, d=8)),  # 2 MB
        # (MemoryProfile.countmin_4096, CountMin(m=1024 * 32 * 8, d=8)),  # 4 MB
        # (MemoryProfile.countmin_8192, CountMin(m=1024 * 32 * 16, d=8)),  # 8 MB
        # (MemoryProfile.countmin_16384, CountMin(m=1024 * 32 * 32, d=8)),  # 16 MB
        # (MemoryProfile.countmin_32768, CountMin(m=1024 * 32 * 64, d=8)),  # 32 MB
        # (MemoryProfile.countmin_65536, CountMin(m=1024 * 32 * 128, d=8)),  # 64 MB

        (MemoryProfile.gsketch_100, GSketch(edge_lists, w=1024 * 6, d=8)),  # 96 KB
        (MemoryProfile.gsketch_200, GSketch(edge_lists, w=1024 * 13, d=8)),  # 208 KB
        (MemoryProfile.gsketch_300, GSketch(edge_lists, w=1024 * 19, d=8)),  # 304 KB
        (MemoryProfile.gsketch_400, GSketch(edge_lists, w=1024 * 25, d=8)),  # 400 KB
        (MemoryProfile.gsketch_512, GSketch(edge_lists, w=1024 * 32, d=8)),  # 512 KB
        # (MemoryProfile.gsketch_1024, GSketch(edge_lists, w=1024 * 32 * 2, d=8)),  # 1 MB
        # (MemoryProfile.gsketch_2048, GSketch(edge_lists, w=1024 * 24 * 4, d=8)),  # 2 MB
        # (MemoryProfile.gsketch_4096, GSketch(edge_lists, w=1024 * 24 * 8, d=8)),  # 4 MB
        # (MemoryProfile.gsketch_8192, GSketch(edge_lists, w=1024 * 24 * 16, d=8)),  # 8 MB
        # (MemoryProfile.gsketch_16384, GSketch(edge_lists, w=1024 * 24 * 32, d=8)),  # 16 MB
        # (MemoryProfile.gsketch_32768, GSketch(edge_lists, w=1024 * 24 * 64, d=8)),  # 32 MB
        # (MemoryProfile.gsketch_65536, GSketch(edge_lists, w=1024 * 24 * 128, d=8)),  # 64 MB

        (MemoryProfile.tcm_100, TCM(w=80, d=8)),  # 100 KB
        (MemoryProfile.tcm_200, TCM(w=113, d=8)),  # 199.5 KB
        (MemoryProfile.tcm_300, TCM(w=139, d=8)),  # 301.8 KB
        (MemoryProfile.tcm_400, TCM(w=160, d=8)),  # 400 KB
        (MemoryProfile.tcm_512, TCM(w=181, d=8)),  # 511.8 KB
        # (MemoryProfile.tcm_1024, TCM(w=256, d=8)),  # 1 MB
        # (MemoryProfile.tcm_2048, TCM(w=362, d=8)),  # 1.9996 MB
        # (MemoryProfile.tcm_4096, TCM(w=512, d=8)),  # 4 MB
        # (MemoryProfile.tcm_8192, TCM(w=724, d=8)),  # 7.9983 MB
        # (MemoryProfile.tcm_16384, TCM(w=1024, d=8)),  # 16 MB
        # (MemoryProfile.tcm_32768, TCM(w=1448, d=8)),  # 31.9932 MB
        # (MemoryProfile.tcm_65536, TCM(w=2048, d=8)),  # 64 MB

        (MemoryProfile.alpha_100, Alpha(edge_lists[0], w=80, d=8)),  # 100 KB
        (MemoryProfile.alpha_200, Alpha(edge_lists[0], w=113, d=8)),  # 199.5 KB
        (MemoryProfile.alpha_300, Alpha(edge_lists[0], w=139, d=8)),  # 301.8 KB
        (MemoryProfile.alpha_400, Alpha(edge_lists[0], w=160, d=8)),  # 400 KB
        (MemoryProfile.alpha_512, Alpha(edge_lists[0], w=181, d=8)),  # 512 KB
        # (MemoryProfile.alpha_1024, Alpha(edge_lists[0], w=256, d=8)),  # 1 MB
        # (MemoryProfile.alpha_2048, Alpha(edge_lists[0], w=362, d=8)),  # 2 MB
        # (MemoryProfile.alpha_4096, Alpha(edge_lists[0], w=512, d=8)),  # 4 MB
        # (MemoryProfile.alpha_8192, Alpha(edge_lists[0], w=724, d=8)),  # 8 MB
        # (MemoryProfile.alpha_16384, Alpha(edge_lists[0], w=1024, d=8)),  # 16 MB
        # (MemoryProfile.alpha_32768, Alpha(edge_lists[0], w=1448, d=8)),  # 32 MB
        # (MemoryProfile.alpha_65536, Alpha(edge_lists[0], w=2048, d=8)),  # 64 MB
    )

    vertices = set()
    edges = set()
    degrees = {}

    for edge_list in edge_lists:
        for edge in edge_list:
            vertices.add(edge[0])  # add source_id
            vertices.add(edge[1])  # add target_id
            edges.add(edge)

            if edge[0] not in degrees:
                degrees[edge[0]] = 1
            else:
                degrees[edge[0]] += 1

            if edge[1] not in degrees:
                degrees[edge[1]] = 1
            else:
                degrees[edge[1]] += 1

    # sort the degrees
    sorted_degrees = sorted(degrees.items(), key=lambda kv: (kv[1], kv[0]))

    number_of_vertices = len(vertices)
    number_of_edges = len(edges)

    test_output_dir = '../output/{}/'.format(os.path.basename(__file__).split('.')[0])
    os.makedirs(os.path.dirname(test_output_dir), exist_ok=True)

    for sketch_id, sketch in memory_profiles:
        # init sketch
        sketch.initialize()
        for edge_list in edge_lists:
            sketch.stream(edge_list)

        sketch_degrees = {}

        # add all vertices
        for vertex in vertices:
            sketch_degrees[vertex] = 0

        for source_id, target_id in edges:
            f = sketch.get_edge_frequency(source_id, target_id)
            sketch_degrees[source_id] += f
            sketch_degrees[target_id] += f

        sorted_sketch_degrees = sorted(sketch_degrees.items(), key=lambda kv: (kv[1], kv[0]))

        # compare top-k results
        k = 1000
        set1 = set([i[0] for i in sorted_degrees[:k]])
        set2 = set([i[0] for i in sorted_sketch_degrees[:k]])
        intersection_count = len(set1.intersection(set2))

        output = {
            'sketch_id': sketch_id.name,
            'sketch_name': sketch.name,
            'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
            'number_of_edges': number_of_edges,
            'number_of_vertices': number_of_vertices,
            'inter_accuracy': intersection_count / k
        }

        with open('{}/{}.json'.format(test_output_dir, sketch_id.name), 'w') as file:
            json.dump(output, file, indent=4)

        print('Completed: {}'.format(sketch_id.name))

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
