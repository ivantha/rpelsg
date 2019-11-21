# Sketch construction time charts

import json
import os

import matplotlib
import matplotlib.pyplot as plt

from sketches import Sketches

if __name__ == '__main__':
    sketches = (
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.alpha.name, 'Alpha'),
    )

    matplotlib.rcParams['figure.dpi'] = 500

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))

    for sketch_name, pretty_name in sketches:
        os.makedirs(os.path.dirname('../output/neq/{}.json'.format(sketch_name)), exist_ok=True)
        with open('../output/neq/{}.json'.format(sketch_name)) as file:
            output = json.load(file)
            results = output['results']
            plt.plot(
                [result['memory_allocation'] for result in results],
                [result['effective_query_count'] for result in results],
                label=pretty_name
            )

    plt.title('Memory vs Number of Effective Queries')
    plt.ylabel('# Effective Queries')
    plt.xlabel('Memory')
    plt.xticks([1024], ('1\nMB'))
    plt.legend()

    os.makedirs(os.path.dirname('../output/neq/{}.json'.format(Sketches.countmin.name)), exist_ok=True)
    with open('../output/neq/{}.json'.format(Sketches.countmin.name)) as file:
        output = json.load(file)
        fig.text(0.1, 0.06, '# base edges : {:,}'.format(output['base_edge_count']))
        fig.text(0.5, 0.06, '# streaming edges : {:,}'.format(output['streaming_edge_count']))
        fig.text(0.5, 0.03, '# queries : 10,000')

    plt.savefig('../output/neq/neq.png')
    plt.show()
