# Heavy nodes (Top 1000)

import gc
import json
import os

from common import utils
from sketches.alpha import Alpha
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM

if __name__ == '__main__':
    base_edges = utils.get_edges_in_path(
        '../datasets/unicorn_wget_small/benign_base/')  # base_path: Path to edges in the base graph
    streaming_edges = utils.get_edges_in_path(
        '../datasets/unicorn_wget_small/benign_streaming/')  # streaming_path: Path to streaming edges

    base_edge_count = len(base_edges)
    streaming_edge_count = len(streaming_edges)

    sketches = (
        FullGraph(),
        CountMin(m=1024 * 32 * 32, d=8),  # 16MB
        GSketch(base_edges, streaming_edges,
                total_sketch_width=1024 * 24 * 32, outlier_sketch_width=1024 * 8 * 32,
                sketch_depth=8),  # 16MB
        TCM(w=256 * 4, d=8),  # 16MB
        Alpha(base_edges, streaming_edges,
              total_sketch_width=887,  # 12.0051 MB
              outlier_sketch_width=512,  # 4 MB
              sketch_depth=8),  # 16MB
    )

    vertices = set()
    edges = set()
    degrees = {}

    for edge in base_edges + streaming_edges:
        vertices.add(edge[0])  # add source_id
        vertices.add(edge[1])  # add target_id
        edges.add(edge)

        if edge[0] not in degrees:
            degrees[edge[0]] = 1
        else:
            degrees[edge[0]] += 1

        if edge[1] not in degrees:
            degrees[edge[1]] = 1
        else:
            degrees[edge[1]] += 1

    # sort the degrees
    sorted_degrees = sorted(degrees.items(), key=lambda kv: (kv[1], kv[0]))

    number_of_vertices = len(vertices)
    number_of_edges = len(edges)

    for sketch in sketches:  # sketches are recreated with increasing memories
        sketch_degrees = {}

        sketch.initialize()  # initialize the sketch
        sketch.stream(base_edges)  # construct base graph
        sketch.stream(streaming_edges)  # streaming edges

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

        print('Completed: {}'.format(sketch.name))

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
