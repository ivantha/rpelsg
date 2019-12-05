# Edge weight distribution

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
        CountMin(m=1024 * 32 * 2, d=8),  # 1MB
        GSketch(base_edges, streaming_edges,
                partitioned_sketch_width=1024 * 24 * 2, outlier_sketch_width=1024 * 8 * 2,
                sketch_depth=8),  # 1MB
        TCM(w=256, d=8),  # 1MB
        Alpha(base_edges, streaming_edges,
              total_sketch_width=222,  # 770 KB
              outlier_sketch_width=128,  # 256 KB
              sketch_depth=8),  # 1MB
    )

    vertices = set()
    edges = set()

    for edge in base_edges + streaming_edges:
        vertices.add(edge[0])  # add source_id
        vertices.add(edge[1])  # add target_id
        edges.add(edge)

    number_of_vertices = len(vertices)
    number_of_edges = len(edges)

    for sketch in sketches:  # sketches are recreated with increasing memories
        edge_weights = {}

        sketch.initialize()  # initialize the sketch
        sketch.stream(base_edges)  # construct base graph
        sketch.stream(streaming_edges)  # streaming edges

        # add all edges
        for source_id, target_id in edges:
            edge_weights['{},{}'.format(source_id, target_id)] = 0

        i = 0
        chunk = number_of_edges / 100
        for source_id, target_id in edges:
            f = sketch.get_edge_frequency(source_id, target_id)
            edge_weights['{},{}'.format(source_id, target_id)] = f

            # update progress bar
            i += 1
            if i % chunk == 0:
                utils.print_progress_bar(i, number_of_edges - 1, prefix='Progress:', suffix=sketch.name, length=50)

        edge_weight_distribution = {}
        for edge_weight in edge_weights.values():
            if edge_weight not in edge_weight_distribution:
                edge_weight_distribution[edge_weight] = edge_weight
            else:
                edge_weight_distribution[edge_weight] += edge_weight

        output = {
            'sketch_name': sketch.name,
            'base_edge_count': base_edge_count,
            'streaming_edge_count': streaming_edge_count,
            'number_of_vertices': number_of_vertices,
            'edge_weights': edge_weights,
            'edge_weight_distribution': edge_weight_distribution
        }

        os.makedirs(os.path.dirname('../output/ewd/{}.json'.format(sketch.name)), exist_ok=True)
        with open('../output/ewd/{}.json'.format(sketch.name), 'w') as file:
            json.dump(output, file, indent=4)

        print('Completed: {}'.format(sketch.name))

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
