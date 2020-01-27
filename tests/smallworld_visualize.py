# small world property

import json
import os

import matplotlib.pyplot as plt

from sketches import Sketches


def smallworld_visualize():
    print(os.path.basename(__file__).split('.')[0])

    sketches = (
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
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
