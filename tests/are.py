# Average Relative Error

import json
import os

from common import utils, sampling
from sketches import Sketches
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM

if __name__ == '__main__':
    # base_path: Path of the sample vertices list that will be used to create the base graph
    base_path = '../datasets/unicorn_wget_small/benign_base/'

    # streaming_path: Path of the vertices list that will be streamed
    streaming_path = '../datasets/unicorn_wget_small/benign_streaming/'

    base_edge_count = utils.get_edge_count(base_path)
    streaming_edge_count = utils.get_edge_count(streaming_path)

    memory_profiles = [
        # TODO : enforce memory profile sizes and "change sketch sizes"
        # 512, 1024 etc.
        # (name, info...)
        # (512, info...)
        ('512', 512),
        # ('1024', 1024)
    ]

    for profile_id, info in memory_profiles:  # sketches are recreated with increasing memories
        # construct a FUllGraph
        full_graph = FullGraph()
        full_graph.initialize()

        full_graph.stream(base_path)  # FullGraph - construct base graph
        full_graph.stream(streaming_path)  # FullGraph - streaming edges

        # Reservoir sampling for 1000 items as (i, j) => 1000 queries
        sample_size = 1000
        sample_stream = sampling.select_k_items(base_path, sample_size)

        sketches = [
            (CountMin(), Sketches.countmin.name),
            (GSketch(base_path, streaming_path), Sketches.gsketch.name),
            (TCM(), Sketches.tcm.name),
        ]

        output = {
            'profile_id' : profile_id,
            'results': []
        }

        for sketch, name in sketches:
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
                'sketch': name,
                'average_relative_error': relative_error_sum / sample_size
            }

            output['results'].append(result)

        os.makedirs(os.path.dirname('../output/are/{}.json'.format(profile_id)), exist_ok=True)
        with open('../output/are/{}.json'.format(profile_id), 'w') as file:
            json.dump(output, file, indent=4)
