# Number of effective queries

import json
import os

import matplotlib
import matplotlib.pyplot as plt

from sketches import Sketches


def neq_visualize():
    print(os.path.basename(__file__).split('.')[0])

    sketches = (
        (Sketches.countmin.name, 'CountMin', [2, 2, 2, 2]),
        (Sketches.gsketch.name, 'gSketch', [2, 2, 10, 2]),
        (Sketches.tcm.name, 'TCM', [5, 2]),
        (Sketches.gmatrix.name, 'GMatrix', [2, 2, 2, 2, 5, 2]),
        (Sketches.alpha.name, 'Alpha', [1, 0]),
    )

    sketch_sizes = (
        (100, '100 KB'),
        (200, '200 KB'),
        (300, '300 KB'),
        (400, '400 KB'),
        (512, '512 KB'),
        # (1024, '1 MB'),
        # (2048, '2 MB'),
        # (4096, '4 MB'),
        # (8192, '8 MB'),
        # (16384, '16 MB'),
        # (32768, '32 MB'),
        # (65536, '64 MB')
    )

    matplotlib.rcParams['figure.dpi'] = 500

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    # ax.set_xscale("log")
    ax.minorticks_off()

    edge_count = 0
    query_count = 0
    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])
    for sketch_name, pretty_name, dashes in sketches:
        memory_allocation = []
        effective_query_count = []

        for sketch_size, pretty_size in sketch_sizes:
            with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                output = json.load(file)
                memory_allocation.append(output['memory_allocation'])
                effective_query_count.append(output['effective_query_count'])
                number_of_edges = output['number_of_edges']
                effective_query_percent = output['effective_query_percent']

        plt.plot(memory_allocation, effective_query_count, label=pretty_name, dashes=dashes)

    plt.title('Memory vs Percentage of Effective Queries')
    plt.ylabel('Percentage of Effective Queries')
    plt.xlabel('Memory')
    plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes])
    plt.legend()

    fig.text(0.1, 0.06, '# edges : {:,}'.format(number_of_edges))
    fig.text(0.5, 0.06, '# queries : {:,}'.format(effective_query_percent))

    test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
    os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
    plt.savefig('../reports/{}/{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name))

    # plt.show()
    plt.close()

