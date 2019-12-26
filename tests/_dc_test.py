# Degree centrality

import gc
import json
import os
import pickle

from common import utils
from tests._memory_profile import MemoryProfile


def dc_test(datasets):
    print('dc_test')

    edge_lists = []
    for dataset in datasets:
        edge_lists.append(utils.get_edges_in_path(dataset))

    memory_profiles = (
        MemoryProfile.fullgraph,

        MemoryProfile.countmin_512,
        MemoryProfile.countmin_1024,
        MemoryProfile.countmin_2048,
        MemoryProfile.countmin_4096,
        MemoryProfile.countmin_8192,
        MemoryProfile.countmin_16384,
        MemoryProfile.countmin_32768,
        MemoryProfile.countmin_65536,

        MemoryProfile.gsketch_512,
        MemoryProfile.gsketch_1024,
        MemoryProfile.gsketch_2048,
        MemoryProfile.gsketch_4096,
        MemoryProfile.gsketch_8192,
        MemoryProfile.gsketch_16384,
        MemoryProfile.gsketch_32768,
        MemoryProfile.gsketch_65536,

        MemoryProfile.tcm_512,
        MemoryProfile.tcm_1024,
        MemoryProfile.tcm_2048,
        MemoryProfile.tcm_4096,
        MemoryProfile.tcm_8192,
        MemoryProfile.tcm_16384,
        MemoryProfile.tcm_32768,
        MemoryProfile.tcm_65536,

        MemoryProfile.alpha_512,
        MemoryProfile.alpha_1024,
        MemoryProfile.alpha_2048,
        MemoryProfile.alpha_4096,
        MemoryProfile.alpha_8192,
        MemoryProfile.alpha_16384,
        MemoryProfile.alpha_32768,
        MemoryProfile.alpha_65536,
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

    for profile in memory_profiles:  # sketches are recreated with increasing memories
        degrees = {}

        # load the sketch
        sketch = pickle.load(open("../pickles/{}.p".format(profile.name), "rb"))

        # add all vertices
        for vertex in vertices:
            degrees[vertex] = 0

        for source_id, target_id in edges:
            f = sketch.get_edge_frequency(source_id, target_id)
            degrees[source_id] += f
            degrees[target_id] += f

        output = {
            'sketch_id': profile.name,
            'sketch_name': sketch.name,
            'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
            'number_of_vertices': number_of_vertices,
            'degrees': degrees
        }

        with open('{}/{}.json'.format(test_output_dir, profile.name), 'w') as file:
            json.dump(output, file, indent=4)

        print('Completed: {}'.format(profile.name))

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
