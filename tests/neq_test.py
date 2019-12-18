# Average Relative Error
import gc
import json
import os

from common import utils, sampling
from sketches import Sketches
from sketches.alpha import Alpha
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM


def neq_test(*argv):
    print('neq_test')

    edge_lists = []
    for arg in argv:
        edge_lists.append(utils.get_edges_in_path(arg))

    memory_profiles = (
        (
            Sketches.countmin.name,
            (
                (512, CountMin(m=1024 * 32, d=8)),  # 512 KB
                (1024, CountMin(m=1024 * 32 * 2, d=8),),  # 1 MB
                (2048, CountMin(m=1024 * 32 * 4, d=8),),  # 2 MB
                (4096, CountMin(m=1024 * 32 * 8, d=8),),  # 4 MB
                (8192, CountMin(m=1024 * 32 * 16, d=8)),  # 8 MB
                (16384, CountMin(m=1024 * 32 * 32, d=8)),  # 16 MB
                (32768, CountMin(m=1024 * 32 * 64, d=8)),  # 32 MB
                (65536, CountMin(m=1024 * 32 * 128, d=8)),  # 64 MB
            )
        ),
        (
            Sketches.gsketch.name,
            (
                (512, GSketch(edge_lists[0],
                              partitioned_sketch_width=1024 * 24, outlier_sketch_width=1024 * 8,
                              sketch_depth=8)),  # 512 KB
                (1024, GSketch(edge_lists[0],
                               partitioned_sketch_width=1024 * 24 * 2, outlier_sketch_width=1024 * 8 * 2,
                               sketch_depth=8)),  # 1 MB
                (2048, GSketch(edge_lists[0],
                               partitioned_sketch_width=1024 * 24 * 4, outlier_sketch_width=1024 * 8 * 4,
                               sketch_depth=8)),  # 2 MB
                (4096, GSketch(edge_lists[0],
                               partitioned_sketch_width=1024 * 24 * 8, outlier_sketch_width=1024 * 8 * 8,
                               sketch_depth=8)),  # 4 MB
                (8192, GSketch(edge_lists[0],
                               partitioned_sketch_width=1024 * 24 * 16, outlier_sketch_width=1024 * 8 * 16,
                               sketch_depth=8)),  # 8 MB
                (16384, GSketch(edge_lists[0],
                                partitioned_sketch_width=1024 * 24 * 32, outlier_sketch_width=1024 * 8 * 32,
                                sketch_depth=8)),  # 16 MB
                (32768, GSketch(edge_lists[0],
                                partitioned_sketch_width=1024 * 24 * 64, outlier_sketch_width=1024 * 8 * 64,
                                sketch_depth=8)),  # 32 MB
                (65536, GSketch(edge_lists[0],
                                partitioned_sketch_width=1024 * 24 * 128, outlier_sketch_width=1024 * 8 * 128,
                                sketch_depth=8)),  # 64 MB
            )
        ),
        (
            Sketches.tcm.name,
            (
                (512, TCM(w=181, d=8)),  # 511.8 KB
                (1024, TCM(w=256, d=8)),  # 1 MB
                (2048, TCM(w=362, d=8)),  # 1.9996 MB
                (4096, TCM(w=512, d=8)),  # 4 MB
                (8192, TCM(w=724, d=8)),  # 7.9983 MB
                (16384, TCM(w=1024, d=8)),  # 16 MB
                (32768, TCM(w=1448, d=8)),  # 31.9932 MB
                (65536, TCM(w=2048, d=8)),  # 64 MB
            )
        ),
        (
            Sketches.alpha.name,
            (
                (512, Alpha(edge_lists[0], total_sketch_width=181, sketch_depth=8)),  # 512 KB
                (1024, Alpha(edge_lists[0], total_sketch_width=256, sketch_depth=8)),  # 1 MB
                (2048, Alpha(edge_lists[0], total_sketch_width=362, sketch_depth=8)),  # 2 MB
                (4096, Alpha(edge_lists[0], total_sketch_width=512, sketch_depth=8)),  # 4 MB
                (8192, Alpha(edge_lists[0], total_sketch_width=724, sketch_depth=8)),  # 8 MB
                (16384, Alpha(edge_lists[0], total_sketch_width=1024, sketch_depth=8)),  # 16 MB
                (32768, Alpha(edge_lists[0], total_sketch_width=1448, sketch_depth=8)),  # 32 MB
                (65536, Alpha(edge_lists[0], total_sketch_width=2048, sketch_depth=8)),  # 64 MB
            )
        ),
    )

    # construct a FullGraph
    full_graph = FullGraph()
    full_graph.initialize()

    for edge_list in edge_lists:
        full_graph.stream(edge_list)

    print('Completed: full_graph')

    # reservoir sampling for 1000 items as (i, j) => 1000 queries
    sample_size = 10000
    sample_stream = sampling.select_k_items(edge_lists[0], sample_size)

    for sketch_name, profiles in memory_profiles:  # sketches are recreated with increasing memories
        output = {
            'sketch_name': sketch_name,
            'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
            'number_of_queries': sample_size,
            'results': []
        }

        for memory_allocation, sketch in profiles:
            sketch.initialize()  # initialize the sketch

            # stream edges
            for edge_list in edge_lists:
                sketch.stream(edge_list)

            # query
            effective_query_count = 0
            for source_id, target_id in sample_stream:
                true_frequency = full_graph.get_edge_frequency(source_id, target_id)
                estimated_frequency = sketch.get_edge_frequency(source_id, target_id)
                if estimated_frequency == true_frequency:
                    effective_query_count += 1

            result = {
                'memory_allocation': memory_allocation,
                'effective_query_count': effective_query_count
            }

            output['results'].append(result)

            # free memory - remove reference to the sketch
            del sketch

            print('Completed: {}_{}'.format(sketch_name, memory_allocation))

        # free memory - call garbage collector
        gc.collect()

        os.makedirs(os.path.dirname('../output/neq/{}.json'.format(sketch_name)), exist_ok=True)
        with open('../output/neq/{}.json'.format(sketch_name), 'w') as file:
            json.dump(output, file, indent=4)
