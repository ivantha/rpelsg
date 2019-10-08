# Sketch construction time

from _datetime import datetime
import os
import json

from common import utils
from sketches.full_graph import FullGraph
from sketches.global_countmin import GlobalCountMin
from sketches.gsketch import GSketch
from sketches.tcm import TCM

if __name__ == '__main__':
    # base_path: Path of the sample vertices list that will be used to create the base graph
    base_path = '../datasets/unicorn_wget_small/benign_base/'

    # streaming_path: Path of the vertices list that will be streamed
    streaming_path = '../datasets/unicorn_wget_small/benign_streaming/'

    base_edge_count = utils.get_edge_count(base_path)
    streaming_edge_count = utils.get_edge_count(streaming_path)

    sketches = [
        (FullGraph(), 'FullGraph'),
        (GlobalCountMin(), 'GlobalCountMin'),
        (GSketch(base_path, streaming_path), 'GSketch'),
        (TCM(), 'TCM'),
    ]

    for sketch, name in sketches:
        process_start_time = datetime.now()

        # initialize the sketch
        initialize_start_time, initialize_end_time = sketch.initialize()

        # construct base graph
        base_start_time = datetime.now()
        for data_file in utils.get_txt_files(base_path):
            with open(data_file) as file:
                for line in file.readlines():
                    source_id, target_id = line.strip().split(',')
                    sketch.add_edge(source_id, target_id)
        base_end_time = datetime.now()

        # streaming edges
        streaming_start_time = datetime.now()
        for data_file in utils.get_txt_files(streaming_path):
            with open(data_file) as file:
                for line in file.readlines():
                    source_id, target_id = line.strip().split(',')
                    sketch.add_edge(source_id, target_id)
        streaming_end_time = datetime.now()

        process_end_time = datetime.now()

        output = {
            'sketch': name,
            'base_edge_count': base_edge_count,
            'streaming_edge_count': streaming_edge_count,
            'initialize_time': '{}'.format(initialize_end_time - initialize_start_time),
            'base_construction_time': '{}'.format(base_end_time - base_start_time),
            'streaming_time': '{}'.format(streaming_end_time - streaming_start_time),
            'process_time': '{}'.format(process_end_time - process_start_time),
        }

        os.makedirs(os.path.dirname('../output/sketch_time/{}.json'.format(name)), exist_ok=True)
        with open('../output/sketch_time/{}.json'.format(name), 'w') as file:
            json.dump(output, file, indent=4)
