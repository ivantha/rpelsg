# Number of effective queries

import json
import os
import pickle

from common import utils, sampling
from tests.memory_profile import MemoryProfile


def neq_test(datasets):
    print('neq_test')

    edge_lists = []
    for dataset in datasets:
        edge_lists.append(utils.get_edges_in_path(dataset))

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

    with open("../pickles/{}.p".format(MemoryProfile.fullgraph.name), "rb") as full_graph_pickle:
        # load a FullGraph
        full_graph = pickle.load(full_graph_pickle)

        # reservoir sampling for 10000 items as (i, j) => 10000 queries
        sample_size = 10000
        sample_stream = sampling.select_k_items(edge_lists[0], sample_size)

        test_output_dir = '../output/{}/'.format(os.path.basename(__file__).split('.')[0])
        os.makedirs(os.path.dirname(test_output_dir), exist_ok=True)

        for profile in memory_profiles:  # sketches are recreated with increasing memories
            with open("../pickles/{}.p".format(profile.name), "rb") as pickled_sketch:
                # load the sketch
                sketch = pickle.load(pickled_sketch)

                # query
                effective_query_count = 0
                for source_id, target_id in sample_stream:
                    true_frequency = full_graph.get_edge_frequency(source_id, target_id)
                    estimated_frequency = sketch.get_edge_frequency(source_id, target_id)
                    if estimated_frequency == true_frequency:
                        effective_query_count += 1

                output = {
                    'sketch_id': profile.name,
                    'sketch_name': profile.name.split('_')[0],
                    'memory_allocation': int(profile.name.split('_')[1]),
                    'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
                    'number_of_queries': sample_size,
                    'effective_query_count': effective_query_count,
                    'effective_query_percent': effective_query_count / sample_size
                }

                with open('{}/{}.json'.format(test_output_dir, profile.name), 'w') as file:
                    json.dump(output, file, indent=4)

                print('Completed: {}'.format(profile.name))

                # free memory - remove reference to the sketch
                # del sketch

                # free memory - call garbage collector
                # gc.collect()
