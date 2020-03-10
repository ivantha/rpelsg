# insertion rate vs amount of data added

import json
import os

import matplotlib.pyplot as plt

from sketches import Sketches


def insertionrate2_visualize():
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
                # (100, '100 KB'),
                # (200, '200 KB'),
                # (300, '300 KB'),
                # (400, '400 KB'),
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
        #     )
        # ),
        # (
        #     3,  # set id
        #     True,  # is log?
        #     (
        #         (8192, '8 MB'),
        #         (16384, '16 MB'),
        #         (32768, '32 MB'),
        #         (65536, '64 MB')
        #     )
        # )
    )

    # insertion rate
    # edge_count = 0
    # test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])
    # for sketch_name, pretty_name in sketches:
    #     for set_id, is_log, sketch_sizes in sketch_sizes_set:
    #         plt.rcParams['figure.dpi'] = 500
    #         plt.rcParams['axes.grid'] = True
    #         plt.rcParams['grid.alpha'] = 0.5
    #         plt.rcParams['grid.color'] = "#cccccc"
    #         # plt.rcParams["figure.figsize"] = (20, 15)
    #
    #         fig = plt.figure()
    #         ax = fig.add_axes((0.15, 0.2, 0.7, 0.7))
    #         # if is_log:
    #         #     ax.set_yscale("log")
    #         # ax.minorticks_off()
    #
    #         # grid for minor ticks
    #         ax.xaxis.grid(True, which='minor')
    #
    #         for sketch_size, pretty_size in sketch_sizes:
    #             with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
    #                 output = json.load(file)
    #                 number_of_edges = output['number_of_edges']
    #                 EDGE_INTERVAL = int(output['EDGE_INTERVAL'])
    #                 streaming_rates = [i / 100000 for i in output['streaming_rates']]
    #
    #             X = [i * EDGE_INTERVAL for i in range(len(streaming_rates))]
    #             plt.plot(X, streaming_rates, label=pretty_size)
    #
    #         plt.title('Number of edges vs Insertion Rate of Edges')
    #         plt.ylabel('Insertion rate (edges/sec) / 10^6')
    #         plt.xlabel('# edges')
    #         # plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes])
    #         plt.legend()
    #
    #         # fig.text(0.1, 0.045, '# edges : {:,}'.format(edge_count))
    #
    #         test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
    #         os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
    #         plt.savefig('../reports/{}/{}_{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], sketch_name, set_id))
    #
    #         # plt.show()
    #         plt.close()
    #
    #         print('Completed visualization: {}_{}'.format(sketch_name, set_id))

    # insertion time
    edge_count = 0
    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])
    for set_id, is_log, sketch_sizes in sketch_sizes_set:
        plt.rcParams['figure.dpi'] = 500
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.5
        plt.rcParams['grid.color'] = "#cccccc"
        # plt.rcParams["figure.figsize"] = (20, 15)

        fig = plt.figure()
        ax = fig.add_axes((0.15, 0.2, 0.7, 0.7))
        # if is_log:
        #     ax.set_yscale("log")
        # ax.minorticks_off()

        # grid for minor ticks
        ax.xaxis.grid(True, which='minor')

        for sketch_size, pretty_size in sketch_sizes:
            for sketch_name, pretty_name, dashes in sketches:
                with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                    output = json.load(file)
                    number_of_edges = output['number_of_edges']
                    EDGE_INTERVAL = int(output['EDGE_INTERVAL'])
                    streaming_times = [i * 100000 for i in output['streaming_times']]

                X = [i * EDGE_INTERVAL / 10000 for i in range(len(streaming_times))]
                plt.plot(X, streaming_times, label=pretty_name, dashes=dashes)

            plt.title('Number of edges vs Insertion time')
            plt.ylabel('Insertion time (sec/edge) / 10^6')
            plt.xlabel('# edges * 10^5')
            # plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes])
            plt.legend()

            fig.text(0.1, 0.045, 'Total # edges : {:,}'.format(number_of_edges))

            test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
            os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
            plt.savefig('../reports/{}/{}_{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name, sketch_size))

            # plt.show()
            plt.close()

            print('Completed visualization: {}_{}'.format(test_name, sketch_size))