# Heavy edges (Top 1000)

import gc
import json
import os

from common import utils
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM

if __name__ == '__main__':
    base_path = '../datasets/unicorn_wget_small/benign_base/'  # base_path: Path to edges in the base graph
    streaming_path = '../datasets/unicorn_wget_small/benign_streaming/'  # streaming_path: Path to streaming edges

    base_edge_count = utils.get_edge_count(base_path)
    streaming_edge_count = utils.get_edge_count(streaming_path)

    sketches = (
        FullGraph(),
        # CountMin(m=1024 * 32 * 8, d=8),  # 4MB
        # GSketch(base_path, streaming_path,
        #         total_sketch_width=1024 * 24 * 8, outlier_sketch_width=1024 * 8 * 8,
        #         sketch_depth=8),  # 4MB
        # TCM(w=256 * 2, d=8),  # 4MB
        CountMin(m=1024 * 32 * 32, d=8),  # 16MB
        GSketch(base_path, streaming_path,
                total_sketch_width=1024 * 24 * 32, outlier_sketch_width=1024 * 8 * 32,
                sketch_depth=8),  # 16MB
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

                    if '{},{}'.format(source_id, target_id) not in edge_weights:
                        edge_weights['{},{}'.format(source_id, target_id)] = 1
                    else:
                        edge_weights['{},{}'.format(source_id, target_id)] += 1

    # sort the edge weights
    sorted_edge_weights = sorted(edge_weights.items(), key=lambda kv: (kv[1], kv[0]))

    number_of_vertices = len(vertices)
    number_of_edges = len(edges)

    for sketch in sketches:  # sketches are recreated with increasing memories
        sketch_edge_weights = {}

        sketch.initialize()  # initialize the sketch
        sketch.stream(base_path)  # construct base graph
        sketch.stream(streaming_path)  # streaming edges

        i = 0
        chunk = number_of_edges / 100
        for source_id, target_id in edges:
            f = sketch.get_edge_frequency(source_id, target_id)
            sketch_edge_weights['{},{}'.format(source_id, target_id)] = f

            # update progress bar
            i += 1
            if i % chunk == 0:
                utils.print_progress_bar(i, number_of_edges - 1, prefix='Progress:', suffix=sketch.name, length=50)

        sorted_sketch_edge_weights = sorted(sketch_edge_weights.items(), key=lambda kv: (kv[1], kv[0]))

        # compare top-k results
        k = 1000
        set1 = set([i[0] for i in sorted_edge_weights[:k]])
        set2 = set([i[0] for i in sorted_sketch_edge_weights[:k]])
        intersection_count = len(set1.intersection(set2))

        output = {
            'sketch_name': sketch.name,
            'base_edge_count': base_edge_count,
            'streaming_edge_count': streaming_edge_count,
            'number_of_edges': number_of_edges,
            'number_of_vertices': number_of_vertices,
            'inter_accuracy': intersection_count / k
        }

        os.makedirs(os.path.dirname('../output/he/{}.json'.format(sketch.name)), exist_ok=True)
        with open('../output/he/{}.json'.format(sketch.name), 'w') as file:
            json.dump(output, file, indent=4)

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
