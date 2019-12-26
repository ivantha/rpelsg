# Heavy edges

import gc
import json
import os
import pickle

from common import utils
from tests.memory_profile import MemoryProfile


def he_test(datasets):
    print('he_test')

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
    edge_weights = {}

    for edge_list in edge_lists:
        for edge in edge_list:
            vertices.add(edge[0])  # add source_id
            vertices.add(edge[1])  # add target_id
            edges.add(edge)

            if '{},{}'.format(edge[0], edge[1]) not in edge_weights:
                edge_weights['{},{}'.format(edge[0], edge[1])] = 1
            else:
                edge_weights['{},{}'.format(edge[0], edge[1])] += 1

    # sort the edge weights
    sorted_edge_weights = sorted(edge_weights.items(), key=lambda kv: (kv[1], kv[0]))

    number_of_vertices = len(vertices)
    number_of_edges = len(edges)

    test_output_dir = '../output/{}/'.format(os.path.basename(__file__).split('.')[0])
    os.makedirs(os.path.dirname(test_output_dir), exist_ok=True)

    for profile in memory_profiles:  # sketches are recreated with increasing memories
        with open("../pickles/{}.p".format(profile.name), "rb") as pickled_sketch:
            # load the sketch
            sketch = pickle.load(pickled_sketch)

            sketch_edge_weights = {}

            i = 0
            chunk = number_of_edges / 100
            for source_id, target_id in edges:
                f = sketch.get_edge_frequency(source_id, target_id)
                sketch_edge_weights['{},{}'.format(source_id, target_id)] = f

                # update progress bar
                i += 1
                if i % chunk == 0:
                    utils.print_progress_bar(i, number_of_edges - 1, prefix='Progress:', suffix=sketch.name, length=50)

            sorted_sketch_edge_weights = sorted(sketch_edge_weights.items(), key=lambda kv: (kv[1], kv[0]))

            # compare top-k results
            k = 1000
            set1 = set([i[0] for i in sorted_edge_weights[:k]])
            set2 = set([i[0] for i in sorted_sketch_edge_weights[:k]])
            intersection_count = len(set1.intersection(set2))

            output = {
                'sketch_id': profile.name,
                'sketch_name': sketch.name,
                'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
                'number_of_edges': number_of_edges,
                'number_of_vertices': number_of_vertices,
                'inter_accuracy': intersection_count / k
            }

            with open('{}/{}.json'.format(test_output_dir, profile.name), 'w') as file:
                json.dump(output, file, indent=4)

            print('Completed: {}'.format(profile.name))

            # free memory - remove reference to the sketch
            # del sketch

            # free memory - call garbage collector
            # gc.collect()