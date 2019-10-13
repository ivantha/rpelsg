# Average Relative Error
import gc
import json
import os

from common import utils, sampling
from sketches import Sketches
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM

if __name__ == '__main__':
    base_path = '../datasets/unicorn_wget_small/benign_base/'  # base_path: Path to edges in the base graph
    streaming_path = '../datasets/unicorn_wget_small/benign_streaming/'  # streaming_path: Path to streaming edges

    base_edge_count = utils.get_edge_count(base_path)
    streaming_edge_count = utils.get_edge_count(streaming_path)

    memory_profiles = (
        (
            Sketches.countmin.name,
            (
                (512, CountMin(m=1024 * 32, d=8)),  # 512KB
                (1024, CountMin(m=1024 * 32 * 2, d=8),),  # 1MB
                (2048, CountMin(m=1024 * 32 * 4, d=8),),  # 2MB
                (4096, CountMin(m=1024 * 32 * 8, d=8),),  # 4MB
                (8192, CountMin(m=1024 * 32 * 16, d=8)),  # 8MB
                (16384, CountMin(m=1024 * 32 * 32, d=8)),  # 16MB
                (32768, CountMin(m=1024 * 32 * 64, d=8)),  # 32MB
                (65536, CountMin(m=1024 * 32 * 128, d=8)),  # 64MB
            )
        ),
        (
            Sketches.gsketch.name,
            (
                (512, GSketch(base_path, streaming_path,
                              total_sketch_width=1024 * 24, outlier_sketch_width=1024 * 8,
                              sketch_depth=8)),  # 512KB
                (1024, GSketch(base_path, streaming_path,
                               total_sketch_width=1024 * 24 * 2, outlier_sketch_width=1024 * 8 * 2,
                               sketch_depth=8)),  # 1MB
                (2048, GSketch(base_path, streaming_path,
                               total_sketch_width=1024 * 24 * 4, outlier_sketch_width=1024 * 8 * 4,
                               sketch_depth=8)),  # 2MB
                (4096, GSketch(base_path, streaming_path,
                               total_sketch_width=1024 * 24 * 8, outlier_sketch_width=1024 * 8 * 8,
                               sketch_depth=8)),  # 4MB
                (8192, GSketch(base_path, streaming_path,
                               total_sketch_width=1024 * 24 * 16, outlier_sketch_width=1024 * 8 * 16,
                               sketch_depth=8)),  # 8MB
                (16384, GSketch(base_path, streaming_path,
                                total_sketch_width=1024 * 24 * 32, outlier_sketch_width=1024 * 8 * 32,
                                sketch_depth=8)),  # 16MB
                (32768, GSketch(base_path, streaming_path,
                                total_sketch_width=1024 * 24 * 64, outlier_sketch_width=1024 * 8 * 64,
                                sketch_depth=8)),  # 32MB
                (65536, GSketch(base_path, streaming_path,
                                total_sketch_width=1024 * 24 * 128, outlier_sketch_width=1024 * 8 * 128,
                                sketch_depth=8)),  # 64MB
            )
        ),
        (
            Sketches.tcm.name,
            (
                (512, TCM(w=256, d=8)),  # 1MB
                (4096, TCM(w=256 * 2, d=8)),  # 4MB
                (16384, TCM(w=256 * 4, d=8)),  # 16MB
                (65536, TCM(w=256 * 8, d=8)),  # 64MB
            )
        )
    )

    # construct a FullGraph
    full_graph = FullGraph()
    full_graph.initialize()

    full_graph.stream(base_path)  # FullGraph - construct base graph
    full_graph.stream(streaming_path)  # FullGraph - streaming edges

    # reservoir sampling for 1000 items as (i, j) => 1000 queries
    sample_size = 1000
    sample_stream = sampling.select_k_items(base_path, sample_size)

    for sketch_name, profiles in memory_profiles:  # sketches are recreated with increasing memories
        output = {
            'sketch_name': sketch_name,
            'results': []
        }

        for memory_allocation, sketch in profiles:
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
                'memory_allocation': memory_allocation,
                'average_relative_error': relative_error_sum / sample_size
            }

            output['results'].append(result)

            # free memory - remove reference to the sketch
            del sketch

        # free memory - call garbage collector
        gc.collect()

        os.makedirs(os.path.dirname('../output/are/{}.json'.format(sketch_name)), exist_ok=True)
        with open('../output/are/{}.json'.format(sketch_name), 'w') as file:
            json.dump(output, file, indent=4)
