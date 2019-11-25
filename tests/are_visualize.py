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
        os.makedirs(os.path.dirname('../output/are/{}.json'.format(sketch_name)), exist_ok=True)
        with open('../output/are/{}.json'.format(sketch_name)) as file:
            output = json.load(file)
            results = output['results']
            plt.plot(
                [result['memory_allocation'] for result in results],
                [result['average_relative_error'] for result in results],
                label=pretty_name
            )

    plt.title('Memory vs Average Relative Error')
    plt.ylabel('Average relative error (%)')
    plt.xlabel('Memory')
    plt.xticks([512, 1024, 2048, 4096, 8192, 16384, 32768, 65536], ('512\nKB', '1\nMB', '2\nMB', '4\nMB', '8\nMB', '16\nMB', '32\nMB', '64\nMB'))
    plt.legend()

    # fig.text(0.1, 0.045, '# base edges : {:,}'.format(results[0]['base_edge_count']))
    # fig.text(0.5, 0.045, '# streaming edges : {:,}'.format(results[0]['streaming_edge_count']))

    plt.savefig('../output/are/are.png')
    plt.show()
