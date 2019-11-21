# Sketch construction time

import json
import os
from datetime import datetime

from common import utils
from sketches.alpha import Alpha
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM

if __name__ == '__main__':
    base_path = '../datasets/unicorn_wget_small/benign_base/'  # base_path: Path to edges in the base graph
    streaming_path = '../datasets/unicorn_wget_small/benign_streaming/'  # streaming_path: Path to streaming edges

    base_edge_count = utils.get_edge_count(base_path)
    streaming_edge_count = utils.get_edge_count(streaming_path)

    # 512KB
    sketches = [
        FullGraph(),
        CountMin(),  # default - 512KB
        GSketch(base_path, streaming_path),  # default - 512KB
        TCM(),  # default - 512KB
        Alpha(base_path, streaming_path),  # default - 512KB
    ]

    # 4MB
    # sketches = [
    #     FullGraph(),
    #     CountMin(m=1024 * 32 * 8, d=8),  # 4MB
    #     GSketch(base_path, streaming_path,
    #             total_sketch_width=1024 * 24 * 8, outlier_sketch_width=1024 * 8 * 8,
    #             sketch_depth=8),  # 4MB
    #     TCM(w=256 * 2, d=8)  # 4MB
    # ]

    for sketch in sketches:
        process_start_time = datetime.now()

        initialize_start_time, initialize_end_time = sketch.initialize()  # initialize the sketch
        base_start_time, base_end_time = sketch.time_critical_stream(base_path)  # construct base graph
        streaming_start_time, streaming_end_time = sketch.time_critical_stream(streaming_path)  # streaming edges

        process_end_time = datetime.now()

        output = {
            'sketch': sketch.name,
            'base_edge_count': base_edge_count,
            'streaming_edge_count': streaming_edge_count,
            'initialize_time': '{}'.format(initialize_end_time - initialize_start_time),
            'base_construction_time': '{}'.format(base_end_time - base_start_time),
            'streaming_time': '{}'.format(streaming_end_time - streaming_start_time),
            'process_time': '{}'.format(process_end_time - process_start_time),
        }

        os.makedirs(os.path.dirname('../output/sketch_time/{}.json'.format(sketch.name)), exist_ok=True)
        with open('../output/sketch_time/{}.json'.format(sketch.name), 'w') as file:
            json.dump(output, file, indent=4)
