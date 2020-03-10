# insertion rate vs memory

import json
import os

import matplotlib.pyplot as plt

from sketches import Sketches


def insertionrate1_visualize():
    print(os.path.basename(__file__).split('.')[0])

    sketches = (
        (Sketches.countmin.name, 'CountMin', [2, 2, 2, 2]),
        (Sketches.gsketch.name, 'gSketch', [2, 2, 10, 2]),
        (Sketches.tcm.name, 'TCM', [5, 2]),
        (Sketches.gmatrix.name, 'GMatrix', [2, 2, 2, 2, 10, 2]),
        (Sketches.alpha.name, 'Alpha', [1, 0]),
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
        # (
        #     2,  # set id
        #     True,  # is log?
        #     (
        #         (512, '512 KB'),
        #         (1024, '1 MB'),
        #         (2048, '2 MB'),
        #         (4096, '4 MB'),
        #         (8192, '8 MB'),
        #         (16384, '16 MB'),
        #         (32768, '32 MB'),
        #         (65536, '64 MB')
        #     )
        # )
    )

    # insertion rate
    # for set_id, is_log, sketch_sizes in sketch_sizes_set:
    #     plt.rcParams['figure.dpi'] = 500
    #     # plt.rcParams["figure.figsize"] = (20, 15)
    #
    #     fig = plt.figure()
    #     ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    #     if is_log:
    #         ax.set_xscale("log")
    #     ax.minorticks_off()
    #
    #     edge_count = 0
    #     test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])
    #     for sketch_name, pretty_name in sketches:
    #         memory_allocation = []
    #         insertions_per_sec = []
    #
    #         for sketch_size, pretty_size in sketch_sizes:
    #             with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
    #                 output = json.load(file)
    #                 memory_allocation.append(output['memory_allocation'])
    #                 insertions_per_sec.append(float(output['insertions_per_sec']) / 1000.0)
    #                 number_of_edges = output['number_of_edges']
    #
    #         plt.plot(memory_allocation, insertions_per_sec, label=pretty_name)
    #
    #     plt.title('Memory vs Insertion Rate of Edges')
    #     plt.ylabel('Insertion rate (edges/sec) * 10^3')
    #     plt.xlabel('Memory')
    #     plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes])
    #     plt.legend()
    #
    #     fig.text(0.1, 0.045, '# edges : {:,}'.format(number_of_edges))
    #
    #     test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
    #     os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
    #     plt.savefig('../reports/{}/{}_{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name, set_id))
    #
    #     # plt.show()
    #     plt.close()
    #
    #     print('Completed visualization: {}_{}'.format(test_name, set_id))

    # insertion time
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
        for sketch_name, pretty_name, dashes in sketches:
            memory_allocation = []
            insertion_time = []

            for sketch_size, pretty_size in sketch_sizes:
                with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                    output = json.load(file)
                    memory_allocation.append(output['memory_allocation'])
                    insertion_time.append(float(output['insertion_time']) * 1000000.0)
                    number_of_edges = output['number_of_edges']

            plt.plot(memory_allocation, insertion_time, label=pretty_name, dashes=dashes)

        plt.title('Memory vs Insertion time')
        plt.ylabel('Insertion time (sec/edge) / 10^6')
        plt.xlabel('Memory')
        plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes])
        plt.legend()

        fig.text(0.1, 0.045, '# edges : {:,}'.format(number_of_edges))

        test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
        os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
        plt.savefig('../reports/{}/{}_{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name, set_id))

        # plt.show()
        plt.close()

        print('Completed visualization: {}_{}'.format(test_name, set_id))