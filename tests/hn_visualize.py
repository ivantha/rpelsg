# Heavy nodes charts

import json
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from sketches import Sketches

if __name__ == '__main__':
    sketches = (
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM')
    )

    results = []

    for sketch_name, pretty_name in sketches:
        os.makedirs(os.path.dirname('../output/hn/{}.json'.format(sketch_name)), exist_ok=True)
        with open('../output/hn/{}.json'.format(sketch_name)) as file:
            output = json.load(file)
            results.append(output)

    matplotlib.rcParams['figure.dpi'] = 500

    ind = np.arange(len(results))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))

    dataset = [x['inter_accuracy'] for x in results]

    plt.bar(ind, dataset, color='#00BCD4')

    plt.title('Heavy nodes')
    plt.ylabel('Inter-accuracy')
    plt.xlabel('Sketches')
    plt.xticks(ind, [pretty_name for sketch_name, pretty_name in sketches])

    fig.text(0.1, 0.06, '# base edges : {:,}'.format(results[0]['base_edge_count']))
    fig.text(0.5, 0.06, '# streaming edges : {:,}'.format(results[0]['streaming_edge_count']))
    fig.text(0.1, 0.03, '# vertices : {:,}'.format(results[0]['number_of_vertices']))
    fig.text(0.5, 0.03, '# edges : {:,}'.format(results[0]['number_of_edges']))

    plt.savefig('../output/hn/hn.png')
    plt.show()
