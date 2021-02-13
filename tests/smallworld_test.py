import gc
import json
import os

import matplotlib.pyplot as plt
import networkx as nx

from common import utils
from sketches import Sketches
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gmatrix import GMatrix
from sketches.gsketch import GSketch
from sketches.kmatrix import Alpha
from sketches.tcm import TCM
from tests.memory_profile import MemoryProfile


def test(datasets):
    print(os.path.basename(__file__).split('.')[0])

    edge_lists = []
    for dataset in datasets:
        edge_lists.append(utils.get_edges_in_path(dataset))

    memory_profiles = (
        (MemoryProfile.fullgraph, FullGraph()),  # 512 KB

        (MemoryProfile.countmin_100, CountMin(m=1024 * 7, d=7)),
        (MemoryProfile.countmin_200, CountMin(m=1024 * 14, d=7)),
        (MemoryProfile.countmin_300, CountMin(m=1024 * 21, d=7)),
        (MemoryProfile.countmin_400, CountMin(m=1024 * 29, d=7)),
        (MemoryProfile.countmin_512, CountMin(m=1024 * 37, d=7)),
        (MemoryProfile.countmin_1024, CountMin(m=1024 * 73, d=7)),
        (MemoryProfile.countmin_2048, CountMin(m=1024 * 146, d=7)),
        (MemoryProfile.countmin_4096, CountMin(m=1024 * 293, d=7)),
        (MemoryProfile.countmin_8192, CountMin(m=1024 * 585, d=7)),
        (MemoryProfile.countmin_16384, CountMin(m=1024 * 1170, d=7)),
        (MemoryProfile.countmin_32768, CountMin(m=1024 * 2341, d=7)),
        (MemoryProfile.countmin_65536, CountMin(m=1024 * 4681, d=7)),
        (MemoryProfile.countmin_131072, CountMin(m=1024 * 9362, d=7)),
        (MemoryProfile.countmin_262144, CountMin(m=1024 * 18725, d=7)),
        (MemoryProfile.countmin_524288, CountMin(m=1024 * 37449, d=7)),
        (MemoryProfile.countmin_1048576, CountMin(m=1024 * 74898, d=7)),

        (MemoryProfile.gsketch_100, GSketch(edge_lists, w=1024 * 7, d=7)),
        (MemoryProfile.gsketch_200, GSketch(edge_lists, w=1024 * 14, d=7)),
        (MemoryProfile.gsketch_300, GSketch(edge_lists, w=1024 * 21, d=7)),
        (MemoryProfile.gsketch_400, GSketch(edge_lists, w=1024 * 29, d=7)),
        (MemoryProfile.gsketch_512, GSketch(edge_lists, w=1024 * 37, d=7)),
        (MemoryProfile.gsketch_1024, GSketch(edge_lists, w=1024 * 73, d=7)),
        (MemoryProfile.gsketch_2048, GSketch(edge_lists, w=1024 * 146, d=7)),
        (MemoryProfile.gsketch_4096, GSketch(edge_lists, w=1024 * 293, d=7)),
        (MemoryProfile.gsketch_8192, GSketch(edge_lists, w=1024 * 585, d=7)),
        (MemoryProfile.gsketch_16384, GSketch(edge_lists, w=1024 * 1170, d=7)),
        (MemoryProfile.gsketch_32768, GSketch(edge_lists, w=1024 * 2341, d=7)),
        (MemoryProfile.gsketch_65536, GSketch(edge_lists, w=1024 * 4681, d=7)),
        (MemoryProfile.gsketch_131072, GSketch(edge_lists, w=1024 * 9362, d=7)),
        (MemoryProfile.gsketch_262144, GSketch(edge_lists, w=1024 * 18725, d=7)),
        (MemoryProfile.gsketch_524288, GSketch(edge_lists, w=1024 * 37449, d=7)),
        (MemoryProfile.gsketch_1048576, GSketch(edge_lists, w=1024 * 74898, d=7)),

        (MemoryProfile.tcm_100, TCM(w=86, d=7)),
        (MemoryProfile.tcm_200, TCM(w=121, d=7)),
        (MemoryProfile.tcm_300, TCM(w=148, d=7)),
        (MemoryProfile.tcm_400, TCM(w=171, d=7)),
        (MemoryProfile.tcm_512, TCM(w=194, d=7)),
        (MemoryProfile.tcm_1024, TCM(w=274, d=7)),
        (MemoryProfile.tcm_2048, TCM(w=387, d=7)),
        (MemoryProfile.tcm_4096, TCM(w=547, d=7)),
        (MemoryProfile.tcm_8192, TCM(w=774, d=7)),
        (MemoryProfile.tcm_16384, TCM(w=1095, d=7)),
        (MemoryProfile.tcm_32768, TCM(w=1548, d=7)),
        (MemoryProfile.tcm_65536, TCM(w=2189, d=7)),
        (MemoryProfile.tcm_131072, TCM(w=3096, d=7)),
        (MemoryProfile.tcm_262144, TCM(w=4379, d=7)),
        (MemoryProfile.tcm_524288, TCM(w=6193, d=7)),
        (MemoryProfile.tcm_1048576, TCM(w=8758, d=7)),

        (MemoryProfile.gmatrix_100, GMatrix(w=86, d=7)),
        (MemoryProfile.gmatrix_200, GMatrix(w=121, d=7)),
        (MemoryProfile.gmatrix_300, GMatrix(w=148, d=7)),
        (MemoryProfile.gmatrix_400, GMatrix(w=171, d=7)),
        (MemoryProfile.gmatrix_512, GMatrix(w=194, d=7)),
        (MemoryProfile.gmatrix_1024, GMatrix(w=274, d=7)),
        (MemoryProfile.gmatrix_2048, GMatrix(w=387, d=7)),
        (MemoryProfile.gmatrix_4096, GMatrix(w=547, d=7)),
        (MemoryProfile.gmatrix_8192, GMatrix(w=774, d=7)),
        (MemoryProfile.gmatrix_16384, GMatrix(w=1095, d=7)),
        (MemoryProfile.gmatrix_32768, GMatrix(w=1548, d=7)),
        (MemoryProfile.gmatrix_65536, GMatrix(w=2189, d=7)),
        (MemoryProfile.gmatrix_131072, GMatrix(w=3096, d=7)),
        (MemoryProfile.gmatrix_262144, GMatrix(w=4379, d=7)),
        (MemoryProfile.gmatrix_524288, GMatrix(w=6193, d=7)),
        (MemoryProfile.gmatrix_1048576, GMatrix(w=8758, d=7)),

        (MemoryProfile.alpha_100, Alpha(edge_lists, w=86, d=7)),
        (MemoryProfile.alpha_200, Alpha(edge_lists, w=121, d=7)),
        (MemoryProfile.alpha_300, Alpha(edge_lists, w=148, d=7)),
        (MemoryProfile.alpha_400, Alpha(edge_lists, w=171, d=7)),
        (MemoryProfile.alpha_512, Alpha(edge_lists, w=194, d=7)),
        (MemoryProfile.alpha_1024, Alpha(edge_lists, w=274, d=7)),
        (MemoryProfile.alpha_2048, Alpha(edge_lists, w=387, d=7)),
        (MemoryProfile.alpha_4096, Alpha(edge_lists, w=547, d=7)),
        (MemoryProfile.alpha_8192, Alpha(edge_lists, w=774, d=7)),
        (MemoryProfile.alpha_16384, Alpha(edge_lists, w=1095, d=7)),
        (MemoryProfile.alpha_32768, Alpha(edge_lists, w=1548, d=7)),
        (MemoryProfile.alpha_65536, Alpha(edge_lists, w=2189, d=7)),
        (MemoryProfile.alpha_131072, Alpha(edge_lists, w=3096, d=7)),
        (MemoryProfile.alpha_262144, Alpha(edge_lists, w=4379, d=7)),
        (MemoryProfile.alpha_524288, Alpha(edge_lists, w=6193, d=7)),
        (MemoryProfile.alpha_1048576, Alpha(edge_lists, w=8758, d=7)),
    )

    nodes = set()
    for edge_list in edge_lists:
        for edge in edge_list:
            nodes.add(edge[0])
            nodes.add(edge[1])

    test_output_dir = '../output/{}/'.format(os.path.basename(__file__).split('.')[0])
    os.makedirs(os.path.dirname(test_output_dir), exist_ok=True)

    for sketch_id, sketch in memory_profiles:
        sketch.initialize()  # initialize the sketch

        # stream edges
        for edge_list in edge_lists:
            sketch.stream(edge_list)

        G = nx.Graph()
        for n1 in nodes:
            for n2 in nodes:
                try:
                    edge_freq = sketch.get_edge_frequency(n1, n2)
                    if edge_freq > 0:
                        G.add_edge(n1, n2, weight=edge_freq)
                except:
                    pass
                    # specific edge is not found in the sketch

        sw_sigma = nx.sigma(G)
        sw_omega = nx.omega(G)
        print('Small world properties of {} is, sigma: {} and omega: {}'.format(sketch_id.name, sw_sigma, sw_omega))

        output = {
            'sketch_id': sketch_id.name,
            'sketch': sketch.name,
            'number_of_edges': sum([len(edge_list) for edge_list in edge_lists]),
            'memory_allocation': 'Inf' if (sketch_id.name == Sketches.fullgraph.name) else int(
                sketch_id.name.split('_')[1]),
            'sw_sigma': sw_sigma,
            'sw_omega': sw_omega
        }

        with open('{}/{}.json'.format(test_output_dir, sketch_id.name), 'w') as file:
            json.dump(output, file, indent=4)

        print('Completed: {}'.format(sketch_id.name))

        # free memory - remove reference to the sketch & G
        del sketch
        del G

        # free memory - call garbage collector
        gc.collect()


def visualize():
    print(os.path.basename(__file__).split('.')[0])

    sketches = (
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.gmatrix.name, 'GMatrix'),
        (Sketches.alpha.name, 'Alpha'),
    )

    sketch_sizes = (
        (1024, '1 MB'),
        (2048, '2 MB'),
        (4096, '4 MB'),
        (8192, '8 MB'),
        (16384, '16 MB'),
        (32768, '32 MB'),
        (65536, '64 MB'),
        (131072, '128 MB'),
        (262144, '256 MB'),
        (524288, '512 MB'),
        (1048576, '1024 MB')
    )

    plt.rcParams['figure.dpi'] = 500
    # plt.rcParams["figure.figsize"] = (20, 15)

    fig1 = plt.figure()
    ax1 = fig1.add_axes((0.1, 0.2, 0.8, 0.7))
    ax1.set_xscale("log")
    ax1.minorticks_off()

    fig2 = plt.figure()
    ax2 = fig2.add_axes((0.1, 0.2, 0.8, 0.7))
    ax2.set_xscale("log")
    ax2.minorticks_off()

    edge_count = 0
    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])
    for sketch_name, pretty_name in sketches:
        memory_allocation = []
        sw_sigma = []
        sw_omega = []

        for sketch_size, pretty_size in sketch_sizes:
            with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                output = json.load(file)
                memory_allocation.append(output['memory_allocation'])
                sw_sigma.append(output['sw_sigma'])
                sw_omega.append(output['sw_omega'])
                number_of_edges = output['number_of_edges']

        plt.figure(1)
        plt.plot(memory_allocation, sw_sigma, label=pretty_name)

        plt.figure(2)
        plt.plot(memory_allocation, sw_omega, label=pretty_name)

    # plot the fullgraph
    with open('{}/{}.json'.format(test_output_dir, Sketches.fullgraph.name)) as file:
        output = json.load(file)
        sw_sigma = output['sw_sigma']
        sw_omega = output['sw_omega']

        plt.figure(1)
        plt.plot([x[0] for x in sketch_sizes], [sw_sigma for x in sketch_sizes], label='FullGraph')

        plt.figure(2)
        plt.plot([x[0] for x in sketch_sizes], [sw_omega for x in sketch_sizes], label='FullGraph')

    plt.figure(1)
    plt.title('Memory vs Small world property')
    plt.ylabel('Small world - sigma')
    plt.xlabel('Memory')
    plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes], rotation='vertical')
    plt.legend()
    fig1.text(0.1, 0.045, '# edges : {:,}'.format(number_of_edges))

    plt.figure(2)
    plt.title('Memory vs Small world property')
    plt.ylabel('Small world - omega')
    plt.xlabel('Memory')
    plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes], rotation='vertical')
    plt.legend()
    fig2.text(0.1, 0.045, '# edges : {:,}'.format(number_of_edges))

    test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
    os.makedirs('../reports/{}'.format(test_name), exist_ok=True)

    plt.figure(1)
    plt.savefig('../reports/{}/{}_sigma.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name))

    plt.figure(2)
    plt.savefig('../reports/{}/{}_omega.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name))

    plt.figure(1)
    # plt.show()
    plt.close()

    plt.figure(2)
    # plt.show()
    plt.close()
