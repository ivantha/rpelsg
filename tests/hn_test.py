# Heavy nodes (Top 1000)

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
    degrees = {}

    for path in (base_path, streaming_path):
        for i, data_file in enumerate(utils.get_txt_files(path)):
            with open(data_file) as file:
                for line in file.readlines():
                    source_id, target_id = line.strip().split(',')

                    vertices.add(source_id)
                    vertices.add(target_id)
                    edges.add((source_id, target_id))

                    if source_id not in degrees:
                        degrees[source_id] = 1
                    else:
                        degrees[source_id] += 1

                    if target_id not in degrees:
                        degrees[target_id] = 1
                    else:
                        degrees[target_id] += 1

    # sort the degrees
    sorted_degrees = sorted(degrees.items(), key=lambda kv: (kv[1], kv[0]))

    number_of_vertices = len(vertices)
    number_of_edges = len(edges)

    for sketch in sketches:  # sketches are recreated with increasing memories
        sketch_degrees = {}

        sketch.initialize()  # initialize the sketch
        sketch.stream(base_path)  # construct base graph
        sketch.stream(streaming_path)  # streaming edges

        # add all vertices
        for vertex in vertices:
            sketch_degrees[vertex] = 0

        i = 0
        chunk = number_of_edges / 100
        for source_id, target_id in edges:
            f = sketch.get_edge_frequency(source_id, target_id)
            sketch_degrees[source_id] += f
            sketch_degrees[target_id] += f

            # update progress bar
            i += 1
            if i % chunk == 0:
                utils.print_progress_bar(i, number_of_edges - 1, prefix='Progress:', suffix=sketch.name, length=50)

        sorted_sketch_degrees = sorted(sketch_degrees.items(), key=lambda kv: (kv[1], kv[0]))

        # compare top-k results
        k = 1000
        set1 = set([i[0] for i in sorted_degrees[:k]])
        set2 = set([i[0] for i in sorted_sketch_degrees[:k]])
        intersection_count = len(set1.intersection(set2))

        output = {
            'sketch_name': sketch.name,
            'base_edge_count': base_edge_count,
            'streaming_edge_count': streaming_edge_count,
            'number_of_edges': number_of_edges,
            'number_of_vertices': number_of_vertices,
            'inter_accuracy': intersection_count / k
        }

        os.makedirs(os.path.dirname('../output/hn/{}.json'.format(sketch.name)), exist_ok=True)
        with open('../output/hn/{}.json'.format(sketch.name), 'w') as file:
            json.dump(output, file, indent=4)

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
