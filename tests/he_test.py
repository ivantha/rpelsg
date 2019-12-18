# Heavy edges (Top 1000)

import gc
import json
import os

from common import utils
from sketches.alpha import Alpha
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM


def he_test(*argv):
    print('he_test')

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

    vertices = set()
    edges = set()
    edge_weights = {}

    for edge_list in edge_lists:
        for edge in edge_list:
            vertices.add(edge[0])  # add source_id
            vertices.add(edge[1])  # add target_id
            edges.add(edge)

            if '{},{}'.format(edge[0], edge[1]) not in edge_weights:
                edge_weights['{},{}'.format(edge[0], edge[1])] = 1
            else:
                edge_weights['{},{}'.format(edge[0], edge[1])] += 1

    # sort the edge weights
    sorted_edge_weights = sorted(edge_weights.items(), key=lambda kv: (kv[1], kv[0]))

    number_of_vertices = len(vertices)
    number_of_edges = len(edges)

    for sketch in sketches:  # sketches are recreated with increasing memories
        sketch_edge_weights = {}

        sketch.initialize()  # initialize the sketch

        # stream edges
        for edge_list in edge_lists:
            sketch.stream(edge_list)

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
            'edge_count': sum([len(edge_list) for edge_list in edge_lists]),
            'number_of_edges': number_of_edges,
            'number_of_vertices': number_of_vertices,
            'inter_accuracy': intersection_count / k
        }

        os.makedirs(os.path.dirname('../output/he/{}.json'.format(sketch.name)), exist_ok=True)
        with open('../output/he/{}.json'.format(sketch.name), 'w') as file:
            json.dump(output, file, indent=4)

        print('Completed: {}'.format(sketch.name))

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()
