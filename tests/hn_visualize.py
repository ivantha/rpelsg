# Heavy nodes

import json
import os

import matplotlib.pyplot as plt
import numpy as np

from sketches import Sketches


def hn_visualize():
    print(os.path.basename(__file__).split('.')[0])

    sketches = (
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.gmatrix.name, 'GMatrix'),
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

    plt.rcParams['figure.dpi'] = 500

    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])

    for sketch_size, pretty_size in sketch_sizes:
        results = []

        for sketch_name, pretty_name in sketches:
            with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                output = json.load(file)
                results.append(output)

        ind = np.arange(len(results))  # the x locations for the groups
        width = 0.35  # the width of the bars

        fig = plt.figure()
        ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))

        dataset = [x['inter_accuracy'] for x in results]

        plt.bar(ind, dataset, color='#00BCD4')

        plt.title('Heavy nodes - {}'.format(pretty_size))
        plt.ylabel('Inter-accuracy')
        plt.xlabel('Sketches')
        plt.xticks(ind, [pretty_name for sketch_name, pretty_name in sketches])

        fig.text(0.1, 0.03, '# vertices : {:,}'.format(results[0]['number_of_vertices']))
        fig.text(0.5, 0.03, '# edges : {:,}'.format(results[0]['number_of_edges']))

        test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
        os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
        plt.savefig('../reports/{}/{}.png'.format(test_name, sketch_size))

        # plt.show()
        plt.close()

        print('Completed visualization: {}'.format(sketch_size))
