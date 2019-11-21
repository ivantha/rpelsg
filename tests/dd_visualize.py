# Degree distribution charts

import json
import os

import matplotlib
import matplotlib.pyplot as plt

from sketches import Sketches

if __name__ == '__main__':
    sketches = (
        (Sketches.full_graph.name, 'FullGraph'),
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.alpha.name, 'Alpha'),
    )

    matplotlib.rcParams['figure.dpi'] = 500

    for sketch_name, pretty_name in sketches:
        os.makedirs(os.path.dirname('../output/dd/{}.json'.format(sketch_name)), exist_ok=True)
        with open('../output/dd/{}.json'.format(sketch_name)) as file:
            output = json.load(file)
            degree_distribution = output['degree_distribution']

            fig = plt.figure()
            ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))

            X = [int(float(i)) for i in degree_distribution.keys()]
            Y = [i for i in degree_distribution.values()]
            plt.scatter(X, Y, marker='.', s=10)

            plt.title('Degree distribution of {}'.format(pretty_name))
            plt.ylabel('Distribution')
            plt.xlabel('Degree')

            fig.text(0.1, 0.06, '# base edges : {:,}'.format(output['base_edge_count']))
            fig.text(0.5, 0.06, '# streaming edges : {:,}'.format(output['streaming_edge_count']))
            fig.text(0.1, 0.03, '# vertices : {:,}'.format(output['number_of_vertices']))

            plt.savefig('../output/dd/dd_{}.png'.format(sketch_name))
            plt.show()
