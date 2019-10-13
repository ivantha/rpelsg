# Sketch construction time charts

import json
import os
from datetime import datetime as dtt

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from sketches import Sketches

if __name__ == '__main__':
    sketches = [
        # Sketches.full_graph.name,
        Sketches.global_countmin.name,
        Sketches.gsketch.name,
        Sketches.tcm.name,
    ]

    results = []

    for sketch_name in sketches:
        os.makedirs(os.path.dirname('../output/sketch_time/{}.json'.format(sketch_name)), exist_ok=True)
        with open('../output/sketch_time/{}.json'.format(sketch_name)) as file:
            output = json.load(file)
            output['initialize_time'] = (dtt.strptime(output['initialize_time'], '%H:%M:%S.%f') - dtt.strptime("00:00","%H:%M")).total_seconds()
            output['base_construction_time'] = (dtt.strptime(output['base_construction_time'], '%H:%M:%S.%f') - dtt.strptime("00:00","%H:%M")).total_seconds()
            output['streaming_time'] = (dtt.strptime(output['streaming_time'], '%H:%M:%S.%f') - dtt.strptime("00:00","%H:%M")).total_seconds()
            results.append(output)

    matplotlib.rcParams['figure.dpi'] = 500

    ind = np.arange(len(results))  # the x locations for the groups
    width = 0.35  # the width of the bars

    dataset = [
        [x['initialize_time'] for x in results],
        [x['base_construction_time'] for x in results],
        [x['streaming_time'] for x in results]
    ]

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.15, 0.8, 0.75))
    # ax.yaxis.grid(True)

    p1 = plt.bar(ind, dataset[0], width, color='#00BCD4')
    p2 = plt.bar(ind, dataset[1], width, bottom=dataset[0], color='#f44336')
    p3 = plt.bar(ind, dataset[2], width, bottom=np.array(dataset[0]) + np.array(dataset[1]), color='#4CAF50')

    plt.title('Sketch construction and streaming times')
    plt.ylabel('Time (s)')
    plt.xticks(ind, ('Full graph', 'CountMin', 'gSketch', 'TCM'))
    plt.legend((p1[0], p2[0], p3[0]), ('Initialization', 'Base construction', 'Streaming'))

    fig.text(0.1, 0.03, '# base edges : {:,}'.format(results[0]['base_edge_count']))
    fig.text(0.5, 0.03, '# streaming edges : {:,}'.format(results[0]['streaming_edge_count']))

    plt.savefig('../output/sketch_time/sketch_time.png')
    plt.show()
