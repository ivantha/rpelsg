# Build time

import json
import os
from datetime import datetime as dtt

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from sketches import Sketches


def buildtime_visualize():
    print(os.path.basename(__file__).split('.')[0].split('_')[0])

    sketches = (
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.alpha.name, 'Alpha'),
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

    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])

    for sketch_size, pretty_size in sketch_sizes:
        results = []

        for sketch_name, pretty_name in sketches:
            with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                output = json.load(file)
                output['initialize_time'] = (
                        dtt.strptime(output['initialize_time'], '%H:%M:%S.%f') - dtt.strptime("00:00", "%H:%M")
                ).total_seconds()
                output['streaming_time'] = (
                        dtt.strptime(output['streaming_time'], '%H:%M:%S.%f') - dtt.strptime("00:00", "%H:%M")
                ).total_seconds()
                results.append(output)

        matplotlib.rcParams['figure.dpi'] = 500

        ind = np.arange(len(results))  # the x locations for the groups
        width = 0.35  # the width of the bars

        dataset = [
            [x['initialize_time'] for x in results],
            [x['streaming_time'] for x in results]
        ]

        fig = plt.figure()
        ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
        # ax.yaxis.grid(True)

        p1 = plt.bar(ind, dataset[0], width, color='#f44336')
        p2 = plt.bar(ind, dataset[1], width, bottom=dataset[0], color='#00BCD4')

        plt.title('Sketch construction and streaming times : {}'.format(pretty_size))
        plt.ylabel('Time (s)')
        plt.xlabel('Sketches')
        plt.xticks(ind, [pretty_name for _, pretty_name in sketches])
        plt.legend((p1[0], p2[0]), ('Initialization', 'Streaming'))

        fig.text(0.1, 0.06, '# edges : {:,}'.format(results[0]['edge_count']))
        fig.text(0.1, 0.03, 'Sketch size : 512 KB')

        test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
        os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
        plt.savefig('../reports/{}/{}_{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name, sketch_size))

        # plt.show()
        plt.close()

        print('Completed visualization: {}'.format(sketch_size))
