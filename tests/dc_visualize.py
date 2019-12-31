# Degree centrality

import json
import os

import matplotlib
import matplotlib.pyplot as plt

from sketches import Sketches


def dc_visualize():
    print('dc_visualize')

    sketches = (
        (Sketches.fullgraph.name, 'FullGraph'),
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.alpha.name, 'Alpha'),
    )

    sketch_sizes = (
        (512, '512 KB'),
        (1024, '1 MB'),
        (2048, '2 MB'),
        (4096, '4 MB'),
        (8192, '8 MB'),
        (16384, '16 MB'),
        (32768, '32 MB'),
        (65536, '64 MB')
    )

    matplotlib.rcParams['figure.dpi'] = 500

    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])

    for sketch_name, pretty_name in sketches:
        for sketch_size, pretty_size in sketch_sizes:
            if sketch_name == Sketches.fullgraph.name:
                if sketch_size == 512:
                    file = open('{}/{}.json'.format(test_output_dir, Sketches.fullgraph.name))
                    sketch_size = ''
                else:
                    break
            else:
                file = open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size))

            output = json.load(file)
            degrees = output['degrees']

            fig = plt.figure()
            ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))

            X = [i for i in degrees.values()]
            plt.hist(X, density=True, bins=100)

            plt.title('Degree centrality histogram of {}'.format(pretty_name))
            plt.ylabel('Frequency')
            plt.xlabel('Degree')

            fig.text(0.5, 0.06, '# edges : {:,}'.format(output['edge_count']))
            fig.text(0.1, 0.03, '# vertices : {:,}'.format(output['number_of_vertices']))

            test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
            os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
            plt.savefig('../reports/{}/{}_{}.png'.format(test_name, sketch_name, sketch_size))

            # plt.show()
            plt.close()

            print('Completed visualization: {}_{}'.format(sketch_name, sketch_size))
