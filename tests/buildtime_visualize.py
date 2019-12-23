# Sketch construction time charts

import json
import os
from datetime import datetime as dtt

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from sketches import Sketches


def buildtime_visualize():
    print('sketch_time_visualize')

    sketches = [
        Sketches.fullgraph.name,
        Sketches.countmin.name,
        Sketches.gsketch.name,
        Sketches.tcm.name,
        Sketches.alpha.name,
    ]

    results = []

    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])
    for sketch_name in sketches:
        with open('{}/{}.json'.format(test_output_dir, sketch_name)) as file:
            output = json.load(file)
            output['initialize_time'] = (dtt.strptime(output['initialize_time'], '%H:%M:%S.%f') - dtt.strptime("00:00",
                                                                                                               "%H:%M")).total_seconds()
            output['streaming_time'] = (dtt.strptime(output['streaming_time'], '%H:%M:%S.%f') - dtt.strptime("00:00",
                                                                                                             "%H:%M")).total_seconds()
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

    plt.title('Sketch construction and streaming times')
    plt.ylabel('Time (s)')
    plt.xlabel('Sketches')
    plt.xticks(ind, ('Full graph', 'CountMin', 'gSketch', 'TCM', 'Alpha'))
    plt.legend((p1[0], p2[0]), ('Initialization', 'Streaming'))

    fig.text(0.1, 0.06, '# edges : {:,}'.format(results[0]['edge_count']))
    fig.text(0.1, 0.03, 'Sketch size : 512 KB')

    os.makedirs('../reports', exist_ok=True)
    plt.savefig('../reports/{}.png'.format(os.path.basename(__file__).split('.')[0]))

    # plt.show()
    plt.close()
