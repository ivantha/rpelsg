# Building the base and the streaming part of the graph

from _datetime import datetime
import os
import json

from common import utils
from sketches import Sketches
from sketches.full_graph import FullGraph
from sketches.global_countmin import GlobalCountMin
from sketches.gsketch import GSketch
from sketches.tcm import TCM


if __name__ == '__main__':
    base_path = '../datasets/unicorn_wget_small/benign_base/'  # base_path: Path to edges in the base graph
    streaming_path = '../datasets/unicorn_wget_small/benign_streaming/'  # streaming_path: Path to streaming edges

    sketches = [
        (FullGraph(), Sketches.full_graph.name),
        (GlobalCountMin(), Sketches.global_countmin.name),
        (GSketch(base_path, streaming_path), Sketches.gsketch.name),
        (TCM(), Sketches.tcm.name),
    ]

    for sketch, name in sketches:
        process_start_time = datetime.now()

        initialize_start_time, initialize_end_time = sketch.initialize()  # initialize the sketch
        base_start_time, base_end_time = sketch.stream(base_path)  # construct base graph
        streaming_start_time, streaming_end_time = sketch.stream(streaming_path)  # streaming edges

        process_end_time = datetime.now()

        analytics_start_time, analytics_end_time, analytics_output = sketch.get_analytics()  # get analytics

        output = {
            'sketch': name,
            'analytics_output': analytics_output,
            'initialize_time': '{}'.format(initialize_end_time - initialize_start_time),
            'base_construction_time': '{}'.format(base_end_time - base_start_time),
            'streaming_time': '{}'.format(streaming_end_time - streaming_start_time),
            'process_time': '{}'.format(process_end_time - process_start_time),
            'analytics_time': '{}'.format(analytics_end_time - analytics_start_time)
        }

        os.makedirs(os.path.dirname('../output/build/{}.json'.format(name)), exist_ok=True)
        with open('../output/build/{}.json'.format(name), 'w') as file:
            json.dump(output, file, indent=4)
