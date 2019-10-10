# Average Relative Error
import gc
import json
import os

from common import utils, sampling
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM

if __name__ == '__main__':
    base_path = '../datasets/unicorn_wget_small/benign_base/'  # base_path: Path to edges in the base graph
    streaming_path = '../datasets/unicorn_wget_small/benign_streaming/'  # streaming_path: Path to streaming edges

    base_edge_count = utils.get_edge_count(base_path)
    streaming_edge_count = utils.get_edge_count(streaming_path)

    memory_profiles = [
        (
            '512kb',
            (
                CountMin(
                    # [2 bytes * (1024 * 32) * 8 = 512 KB]
                    m=1024 * 32,  # m: Size of the hash table (➡️)
                    d=8  # d: Number of hash functions (⬇️)
                ),
                GSketch(
                    base_path,
                    streaming_path,

                    # partitioned sketch => [2 bytes * (1024 * 16) * 8 = 256 KB]
                    sketch_total_width=1024 * 16,  # m: Total width of the hash table (➡️)
                    sketch_depth=8,  # d: Number of hash functions (⬇️)

                    # outliers => [2 bytes * (1024 * 16) * 8 = 256 KB]
                    outlier_sketch_width=1024 * 16,  # Width of the outlier hash table (➡️)
                ),
                TCM(
                    # [2 bytes * (256 * 256) * 4 = 512 KB)]
                    w=256,  # w: Side width of the hash tables (size = ↓w * →w)
                    d=4  # d: Number of hash functions
                ),
            )
        ),
        (
            '2mb',
            (
                CountMin(
                    m=1024 * 32 * 4,
                    d=8
                ),
                GSketch(
                    base_path,
                    streaming_path,
                    sketch_total_width=1024 * 16 * 2,
                    sketch_depth=8,
                    outlier_sketch_width=1024 * 16 * 2,
                ),
                TCM(
                    w=256 * 2,
                    d=4
                ),
                TCM(
                    w=256,
                    d=4 * 4
                ),
            )
        ),
        (
            '8mb',
            (
                CountMin(
                    m=1024 * 32 * 8,
                    d=8 * 2
                ),
                GSketch(
                    base_path,
                    streaming_path,
                    sketch_total_width=1024 * 16 * 4,
                    sketch_depth=8,
                    outlier_sketch_width=1024 * 16 * 4,
                ),
                TCM(
                    w=256 * 2,
                    d=4 * 4
                ),
            )
        ),
        (
            '32mb',
            (
                CountMin(
                    m=1024 * 32 * 32,
                    d=8 * 2
                ),
                GSketch(
                    base_path,
                    streaming_path,
                    sketch_total_width=1024 * 16 * 8,
                    sketch_depth=8 * 2,
                    outlier_sketch_width=1024 * 16 * 8,
                ),
                TCM(
                    w=256 * 4,
                    d=4 * 4
                ),
            )
        ),
        (
            '128mb',
            (
                TCM(
                    w=256 * 8,
                    d=4 * 4
                ),
            )
        ),
    ]

    for profile_id, sketches in memory_profiles:  # sketches are recreated with increasing memories
        # construct a FullGraph
        full_graph = FullGraph()
        full_graph.initialize()

        full_graph.stream(base_path)  # FullGraph - construct base graph
        full_graph.stream(streaming_path)  # FullGraph - streaming edges

        # reservoir sampling for 1000 items as (i, j) => 1000 queries
        sample_size = 1000
        sample_stream = sampling.select_k_items(base_path, sample_size)

        output = {
            'profile_id': profile_id,
            'results': []
        }

        for sketch in sketches:
            initialize_start_time, initialize_end_time = sketch.initialize()  # initialize the sketch
            base_start_time, base_end_time = sketch.stream(base_path)  # construct base graph
            streaming_start_time, streaming_end_time = sketch.stream(streaming_path)  # streaming edges

            # query
            relative_error_sum = 0
            for source_id, target_id in sample_stream:
                true_frequency = full_graph.get_edge_frequency(source_id, target_id)
                estimated_frequency = sketch.get_edge_frequency(source_id, target_id)
                relative_error = (estimated_frequency - true_frequency) / true_frequency * 1.0
                relative_error_sum += relative_error

            result = {
                'sketch': sketch.name,
                'average_relative_error': relative_error_sum / sample_size
            }

            output['results'].append(result)

            # TODO : Properly dereference the object
            # free memory - remove reference to the sketch
            sketch = None

        # free memory - call garbage collector
        gc.collect()

        os.makedirs(os.path.dirname('../output/are/{}.json'.format(profile_id)), exist_ok=True)
        with open('../output/are/{}.json'.format(profile_id), 'w') as file:
            json.dump(output, file, indent=4)
