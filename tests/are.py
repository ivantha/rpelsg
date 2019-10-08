# Average Relative Error

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

    memory_profiles = [
        # TODO
        # 512, 1024 etc.
        # (name, info...)
        # (512, info...)
    ]

    for name, info in memory_profiles:  # sketches are recreated with increasing memories
        # TODO : compute full graph

        sketches = [
            (GlobalCountMin(), 'GlobalCountMin'),
            (GSketch(base_path, streaming_path), 'GSketch'),
            (TCM(), 'TCM'),
        ]

        output = {
            'name' : name,
            'results': []
        }

        for sketch, name in sketches:
            # initialize the sketch
            sketch.initialize()

            # construct base graph
            for data_file in utils.get_txt_files(base_path):
                with open(data_file) as file:
                    for line in file.readlines():
                        source_id, target_id = line.strip().split(',')
                        sketch.add_edge(source_id, target_id)

            # streaming edges
            for data_file in utils.get_txt_files(streaming_path):
                with open(data_file) as file:
                    for line in file.readlines():
                        source_id, target_id = line.strip().split(',')
                        sketch.add_edge(source_id, target_id)

            # TODO : QUERY

            result = {
                'sketch': name,
                # TODO : value
            }

            output['results'].append(result)

        os.makedirs(os.path.dirname('../output/are/{}.json'.format(name)), exist_ok=True)
        with open('../output/are/{}.json'.format(name), 'w') as file:
            json.dump(output, file, indent=4)
