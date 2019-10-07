# Memory x Sketch construction time

from _datetime import datetime
import os

from common import utils
from sketches.full_graph import FullGraph
from sketches.global_countmin import GlobalCountMin
from sketches.gsketch import GSketch
from sketches.tcm import TCM


def test(sketch, name):
    process_start_time = datetime.now()

    # initialize the sketch
    initialize_start_time, initialize_end_time = sketch.initialize()

    # construct base graph
    base_start_time = datetime.now()
    data_files = utils.get_txt_files(base_path)
    for data_file in data_files:
        with open(data_file) as file:
            for line in file.readlines():
                source_id, target_id = line.strip().split(',')
                sketch.add_edge(source_id, target_id)
    base_end_time = datetime.now()

    # streaming edges
    streaming_start_time = datetime.now()
    data_files = utils.get_txt_files(streaming_path)
    for data_file in data_files:
        with open(data_file) as file:
            for line in file.readlines():
                source_id, target_id = line.strip().split(',')
                sketch.add_edge(source_id, target_id)
    streaming_end_time = datetime.now()

    os.makedirs(os.path.dirname('../output/mem_time/{}.txt'.format(name)), exist_ok=True)
    with open('../output/mem_time/{}.txt'.format(name), 'w') as file:
        file.write('Benchmark results : {}\n'.format(name))

        # print analytics
        analytics_start_time, analytics_end_time = sketch.print_analytics(file)

        # calculate time
        initialize_time = initialize_end_time - initialize_start_time
        base_time = base_end_time - base_start_time
        streaming_time = streaming_end_time - streaming_start_time
        analytics_time = analytics_end_time - analytics_start_time
        process_time = datetime.now() - process_start_time

        file.write('\nInitialize time: {} ({:.2f}%)\n'.format(initialize_time, (initialize_time / process_time * 100.0)))
        file.write('Base graph construction time: {} ({:.2f}%)\n'.format(base_time, (base_time / process_time * 100.0)))
        file.write('Streaming time: {} ({:.2f}%)\n'.format(streaming_time, (streaming_time / process_time * 100.0)))
        file.write('Analytics time: {} ({:.2f}%)\n'.format(analytics_time, (analytics_time / process_time * 100)))
        file.write('Total process time: {}\n'.format(process_time))


if __name__ == '__main__':
    # base_path: Path of the sample vertices list that will be used to create the base graph
    base_path = '../datasets/unicorn_wget_small/benign_base/'

    # streaming_path: Path of the vertices list that will be streamed
    streaming_path = '../datasets/unicorn_wget_small/benign_streaming/'

    sketches = [
        (FullGraph(), 'FullGraph'),
        (GlobalCountMin(), 'GlobalCountMin'),
        (GSketch(base_path, streaming_path), 'GSketch'),
        (TCM(), 'TCM'),
    ]

    results = []
    for sketch, name in sketches:
        result = test(sketch, name)
        results.append(result)