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


def sketch_time_test(*argv):
    print('sketch_time_test')

    edge_lists = []
    for arg in argv:
        edge_lists.append(utils.get_edges_in_path(arg))

    sketches = (
        FullGraph(),
        CountMin(m=1024 * 32 * 2, d=8),  # 1MB
        GSketch(edge_lists[0],
                partitioned_sketch_width=1024 * 24 * 2, outlier_sketch_width=1024 * 8 * 2, sketch_depth=8),  # 1MB
        TCM(w=256, d=8),  # 1MB
        Alpha(edge_lists[0], total_sketch_width=256, sketch_depth=8),  # 1MB
    )

    for sketch in sketches:
        process_start_time = datetime.now()

        initialize_start_time, initialize_end_time = sketch.initialize()  # initialize the sketch

        streaming_times = []
        for edge_list in edge_lists:
            streaming_times.append(sketch.stream(edge_list))

        streaming_start_time = streaming_times[0][0]
        streaming_end_time = streaming_times[-1][1]

        process_end_time = datetime.now()

        output = {
            'sketch': sketch.name,
            'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
            'initialize_time': '{}'.format(initialize_end_time - initialize_start_time),
            'streaming_time': '{}'.format(streaming_end_time - streaming_start_time),
            'process_time': '{}'.format(process_end_time - process_start_time),
        }

        os.makedirs(os.path.dirname('../output/sketch_time/{}.json'.format(sketch.name)), exist_ok=True)
        with open('../output/sketch_time/{}.json'.format(sketch.name), 'w') as file:
            json.dump(output, file, indent=4)
