# Average relative error

import gc
import json
import os
import pickle

from common import utils, sampling
from tests._memory_profile import MemoryProfile


def are_test(*argv):
    print('are_test')

    edge_lists = []
    for arg in argv:
        edge_lists.append(utils.get_edges_in_path(arg))

    memory_profiles = (
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

    # load a FullGraph
    full_graph = pickle.load(open("../pickles/{}.p".format(MemoryProfile.fullgraph.name), "rb"))

    # reservoir sampling for 1000 items as (i, j) => 1000 queries
    sample_size = 1000
    sample_stream = sampling.select_k_items(edge_lists[0], sample_size)

    test_output_dir = '../output/{}/'.format(os.path.basename(__file__).split('.')[0])
    os.makedirs(os.path.dirname(test_output_dir), exist_ok=True)

    for profile in memory_profiles:  # sketches are recreated with increasing memories
        # load the sketch
        sketch = pickle.load(open("../pickles/{}.p".format(profile.name), "rb"))

        # query
        relative_error_sum = 0
        for source_id, target_id in sample_stream:
            true_frequency = full_graph.get_edge_frequency(source_id, target_id)
            estimated_frequency = sketch.get_edge_frequency(source_id, target_id)
            relative_error = (estimated_frequency - true_frequency) / true_frequency * 1.0
            relative_error_sum += relative_error

        output = {
            'sketch_id': profile.name,
            'sketch_name': sketch.name,
            'memory_allocation': int(profile.name.split('_')[1]),
            'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
            'average_relative_error': relative_error_sum / sample_size
        }

        with open('{}/{}.json'.format(test_output_dir, profile.name), 'w') as file:
            json.dump(output, file, indent=4)

        print('Completed: {}'.format(profile.name))

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
