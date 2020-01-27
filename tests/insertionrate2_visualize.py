# insertion rate vs amount of data added

import json
import os

import matplotlib.pyplot as plt

from sketches import Sketches


def insertionrate2_visualize():
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
            )
        ),
        (
            3,  # set id
            True,  # is log?
            (
                (8192, '8 MB'),
                (16384, '16 MB'),
                (32768, '32 MB'),
                (65536, '64 MB')
            )
        )
    )

    edge_count = 0
    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])
    for sketch_name, pretty_name in sketches:
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
                with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                    output = json.load(file)
                    edge_count = output['edge_count']
                    EDGE_INTERVAL = int(output['EDGE_INTERVAL'])
                    streaming_rates = [i / 100000 for i in output['streaming_rates']]

                X = [i * EDGE_INTERVAL for i in range(len(streaming_rates))]
                plt.plot(X, streaming_rates, label=pretty_size)

            plt.title('Number of edges vs Insertion Rate of Edges')
            plt.ylabel('Insertion rate (edges/sec) / 10^6')
            plt.xlabel('# edges')
            # plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes])
            plt.legend()

            # fig.text(0.1, 0.045, '# edges : {:,}'.format(edge_count))

            test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
            os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
            plt.savefig('../reports/{}/{}_{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], sketch_name, set_id))

            # plt.show()
            plt.close()

            print('Completed visualization: {}_{}'.format(sketch_name, set_id))