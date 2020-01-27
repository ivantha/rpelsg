# insertion rate vs memory

import json
import os

import matplotlib.pyplot as plt

from sketches import Sketches


def insertionrate1_visualize():
    print(os.path.basename(__file__).split('.')[0])

    sketches = (
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.alpha.name, 'Alpha'),
    )

    sketch_sizes_set = (
        (
            1,  # set id
            False,  # is log?
            (
                (100, '100 KB'),
                (200, '200 KB'),
                (300, '300 KB'),
                (400, '400 KB'),
                (512, '512 KB'),
            )
        ),
        (
            2,  # set id
            True,  # is log?
            (
                (512, '512 KB'),
                (1024, '1 MB'),
                (2048, '2 MB'),
                (4096, '4 MB'),
                (8192, '8 MB'),
                (16384, '16 MB'),
                (32768, '32 MB'),
                (65536, '64 MB')
            )
        )
    )

    for set_id, is_log, sketch_sizes in sketch_sizes_set:
        plt.rcParams['figure.dpi'] = 500
        # plt.rcParams["figure.figsize"] = (20, 15)

        fig = plt.figure()
        ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
        if is_log:
            ax.set_xscale("log")
        ax.minorticks_off()

        edge_count = 0
        test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])
        for sketch_name, pretty_name in sketches:
            memory_allocation = []
            insertions_per_sec = []

            for sketch_size, pretty_size in sketch_sizes:
                with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                    output = json.load(file)
                    memory_allocation.append(output['memory_allocation'])
                    insertions_per_sec.append(float(output['insertions_per_sec']) / 1000.0)
                    edge_count = output['edge_count']

            plt.plot(memory_allocation, insertions_per_sec, label=pretty_name)

        plt.title('Memory vs Insertion Rate of Edges')
        plt.ylabel('Insertion rate (edges/sec) * 10^3')
        plt.xlabel('Memory')
        plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes])
        plt.legend()

        fig.text(0.1, 0.045, '# edges : {:,}'.format(edge_count))

        test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
        os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
        plt.savefig('../reports/{}/{}_{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name, set_id))

        # plt.show()
        plt.close()

        print('Completed visualization: {}_{}'.format(test_name, set_id))