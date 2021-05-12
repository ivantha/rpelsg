import gc
import json
import os

import matplotlib.pyplot as plt

from common import utils
from sketches import Sketches
from sketches.countmin import CountMin
from sketches.gmatrix import GMatrix
from sketches.gsketch import GSketch
from sketches.kmatrix import Alpha
from sketches.tcm import TCM
from tests.memory_profile import MemoryProfile

EDGE_INTERVAL = 10000


def test(datasets):
    print(os.path.basename(__file__).split('.')[0])

    edge_lists = []
    for dataset in datasets:
        edge_lists.append(utils.get_edges_in_path(dataset))

    memory_profiles = (
        (MemoryProfile.countmin_100, CountMin(m=1024 * 7, d=7)),
        (MemoryProfile.countmin_200, CountMin(m=1024 * 14, d=7)),
        (MemoryProfile.countmin_300, CountMin(m=1024 * 21, d=7)),
        (MemoryProfile.countmin_400, CountMin(m=1024 * 29, d=7)),
        (MemoryProfile.countmin_512, CountMin(m=1024 * 37, d=7)),
        # (MemoryProfile.countmin_1024, CountMin(m=1024 * 73, d=7)),
        # (MemoryProfile.countmin_2048, CountMin(m=1024 * 146, d=7)),
        # (MemoryProfile.countmin_4096, CountMin(m=1024 * 293, d=7)),
        # (MemoryProfile.countmin_8192, CountMin(m=1024 * 585, d=7)),
        # (MemoryProfile.countmin_16384, CountMin(m=1024 * 1170, d=7)),
        # (MemoryProfile.countmin_32768, CountMin(m=1024 * 2341, d=7)),
        # (MemoryProfile.countmin_65536, CountMin(m=1024 * 4681, d=7)),

        (MemoryProfile.gsketch_100, GSketch(edge_lists, w=1024 * 7, d=7)),
        (MemoryProfile.gsketch_200, GSketch(edge_lists, w=1024 * 14, d=7)),
        (MemoryProfile.gsketch_300, GSketch(edge_lists, w=1024 * 21, d=7)),
        (MemoryProfile.gsketch_400, GSketch(edge_lists, w=1024 * 29, d=7)),
        (MemoryProfile.gsketch_512, GSketch(edge_lists, w=1024 * 37, d=7)),
        # (MemoryProfile.gsketch_1024, GSketch(edge_lists, w=1024 * 73, d=7)),
        # (MemoryProfile.gsketch_2048, GSketch(edge_lists, w=1024 * 146, d=7)),
        # (MemoryProfile.gsketch_4096, GSketch(edge_lists, w=1024 * 293, d=7)),
        # (MemoryProfile.gsketch_8192, GSketch(edge_lists, w=1024 * 585, d=7)),
        # (MemoryProfile.gsketch_16384, GSketch(edge_lists, w=1024 * 1170, d=7)),
        # (MemoryProfile.gsketch_32768, GSketch(edge_lists, w=1024 * 2341, d=7)),
        # (MemoryProfile.gsketch_65536, GSketch(edge_lists, w=1024 * 4681, d=7)),

        (MemoryProfile.tcm_100, TCM(w=86, d=7)),
        (MemoryProfile.tcm_200, TCM(w=121, d=7)),
        (MemoryProfile.tcm_300, TCM(w=148, d=7)),
        (MemoryProfile.tcm_400, TCM(w=171, d=7)),
        (MemoryProfile.tcm_512, TCM(w=194, d=7)),
        # (MemoryProfile.tcm_1024, TCM(w=274, d=7)),
        # (MemoryProfile.tcm_2048, TCM(w=387, d=7)),
        # (MemoryProfile.tcm_4096, TCM(w=547, d=7)),
        # (MemoryProfile.tcm_8192, TCM(w=774, d=7)),
        # (MemoryProfile.tcm_16384, TCM(w=1095, d=7)),
        # (MemoryProfile.tcm_32768, TCM(w=1548, d=7)),
        # (MemoryProfile.tcm_65536, TCM(w=2189, d=7)),

        (MemoryProfile.gmatrix_100, GMatrix(w=86, d=7)),
        (MemoryProfile.gmatrix_200, GMatrix(w=121, d=7)),
        (MemoryProfile.gmatrix_300, GMatrix(w=148, d=7)),
        (MemoryProfile.gmatrix_400, GMatrix(w=171, d=7)),
        (MemoryProfile.gmatrix_512, GMatrix(w=194, d=7)),
        # (MemoryProfile.gmatrix_1024, GMatrix(w=274, d=7)),
        # (MemoryProfile.gmatrix_2048, GMatrix(w=387, d=7)),
        # (MemoryProfile.gmatrix_4096, GMatrix(w=547, d=7)),
        # (MemoryProfile.gmatrix_8192, GMatrix(w=774, d=7)),
        # (MemoryProfile.gmatrix_16384, GMatrix(w=1095, d=7)),
        # (MemoryProfile.gmatrix_32768, GMatrix(w=1548, d=7)),
        # (MemoryProfile.gmatrix_65536, GMatrix(w=2189, d=7)),

        (MemoryProfile.alpha_100, Alpha(edge_lists, w=86, d=7)),
        (MemoryProfile.alpha_200, Alpha(edge_lists, w=121, d=7)),
        (MemoryProfile.alpha_300, Alpha(edge_lists, w=148, d=7)),
        (MemoryProfile.alpha_400, Alpha(edge_lists, w=171, d=7)),
        (MemoryProfile.alpha_512, Alpha(edge_lists, w=194, d=7)),
        # (MemoryProfile.alpha_1024, Alpha(edge_lists, w=274, d=7)),
        # (MemoryProfile.alpha_2048, Alpha(edge_lists, w=387, d=7)),
        # (MemoryProfile.alpha_4096, Alpha(edge_lists, w=547, d=7)),
        # (MemoryProfile.alpha_8192, Alpha(edge_lists, w=774, d=7)),
        # (MemoryProfile.alpha_16384, Alpha(edge_lists, w=1095, d=7)),
        # (MemoryProfile.alpha_32768, Alpha(edge_lists, w=1548, d=7)),
        # (MemoryProfile.alpha_65536, Alpha(edge_lists, w=2189, d=7)),
    )

    n_edges = sum([len(edge_list) for edge_list in edge_lists])

    # create a new list of <EDGE_INTERVAL>-edge lists
    new_edge_lists = []
    for edge_list in edge_lists:
        new_edge_list = []
        i = 0
        for edge in edge_list:
            if i == EDGE_INTERVAL:
                new_edge_lists.append(new_edge_list)
                new_edge_list = []
                i = 0
            else:
                new_edge_list.append(edge)
                i += 1

    test_output_dir = '../output/{}/'.format(os.path.basename(__file__).split('.')[0])
    os.makedirs(os.path.dirname(test_output_dir), exist_ok=True)

    for sketch_id, sketch in memory_profiles:
        sketch.initialize()  # initialize the sketch

        # stream edges
        streaming_times = []
        for edge_list in new_edge_lists:
            streaming_times.append(sketch.stream(edge_list))

        streaming_rates = []
        streaming_times_per_edge = []
        for i in range(1, len(streaming_times) - 1):  # remove the first and last EDGE_INTERVAL blocks
            streaming_rates.append(EDGE_INTERVAL / (streaming_times[i][1] - streaming_times[i][0]).total_seconds())
            streaming_times_per_edge.append(
                (streaming_times[i][1] - streaming_times[i][0]).total_seconds() / EDGE_INTERVAL)

        output = {
            'sketch_id': sketch_id.name,
            'sketch_name': sketch.name,
            'memory_allocation': int(sketch_id.name.split('_')[1]),
            'number_of_edges': n_edges,
            'EDGE_INTERVAL': EDGE_INTERVAL,
            'streaming_rates': streaming_rates,
            'streaming_times': streaming_times_per_edge
        }

        sketch.print_analytics()

        with open('{}/{}.json'.format(test_output_dir, sketch_id.name), 'w') as file:
            json.dump(output, file, indent=4)

        print('Completed: {}'.format(sketch_id.name))

        # free memory - remove reference to the sketch
        del sketch

        # free memory - call garbage collector
        gc.collect()


def visualize():
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
            plt.savefig(
                '../reports/{}/{}_{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name,
                                                 sketch_size))

            # plt.show()
            plt.close()

            print('Completed visualization: {}_{}'.format(test_name, sketch_size))
