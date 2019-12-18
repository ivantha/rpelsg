# Reachability

import gc
import json
import os
import random

from common import utils
from sketches.full_graph import FullGraph
from sketches.tcm import TCM


def reachability_test():
    base_path = '../datasets/unicorn_wget_small/benign_base/'  # base_path: Path to edges in the base graph
    streaming_path = '../datasets/unicorn_wget_small/benign_streaming/'  # streaming_path: Path to streaming edges

    base_edge_count = utils.get_edge_count(base_path)
    streaming_edge_count = utils.get_edge_count(streaming_path)

    sketches = (
        FullGraph(),
        TCM(w=256 * 4, d=8),  # 16MB
    )

    vertices = set()
    edges = set()
    edge_weights = {}

    for path in (base_path, streaming_path):
        for i, data_file in enumerate(utils.get_txt_files(path)):
            with open(data_file) as file:
                for line in file.readlines():
                    source_id, target_id = line.strip().split(',')

                    vertices.add(source_id)
                    vertices.add(target_id)
                    edges.add((source_id, target_id))

    # resevoir sampling for vertices
    k = 200
    i = 0
    reservoir = [0] * k
    for vertex in vertices:
        if i < k:
            reservoir[i] = vertex
        else:
            j = random.randrange(i + 1)
            if j < k:
                reservoir[j] = vertex
        i += 1

    reservoir = list(zip(reservoir[:100], reservoir[100:]))

    for sketch in sketches:  # sketches are recreated with increasing memories
        sketch_edge_weights = {}

        sketch.initialize()  # initialize the sketch
        sketch.stream(base_path)  # construct base graph
        sketch.stream(streaming_path)  # streaming edges

        # compare top-k results
        k = 1000
        set1 = set([i[0] for i in sorted_edge_weights[:k]])
        set2 = set([i[0] for i in sorted_sketch_edge_weights[:k]])
        intersection_count = len(set1.intersection(set2))

        output = {
            'sketch_name': sketch.name,
            'base_edge_count': base_edge_count,
            'streaming_edge_count': streaming_edge_count,
            'inter_accuracy': intersection_count / k
        }

        os.makedirs(os.path.dirname('../output/reachability/{}.json'.format(sketch.name)), exist_ok=True)
        with open('../output/reachability/{}.json'.format(sketch.name), 'w') as file:
            json.dump(output, file, indent=4)

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
