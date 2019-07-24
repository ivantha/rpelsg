from _datetime import datetime
import os

from sketches.full_graph import FullGraph
from sketches.global_countmin import GlobalCountMin
from sketches.gsketch import GSketch
from sketches.tcm import TCM


def test(sketch, name):
    process_start_time = datetime.now()

    sketch = sketch(base_path='../datasets/unicorn_wget_small/benign_base/',
                    streaming_path='../datasets/unicorn_wget_small/benign_streaming/')

    # construct base graph
    base_start_time, base_end_time = sketch.construct_base_graph()

    # streaming edges
    streaming_start_time, streaming_end_time = sketch.construct_stream_graph()

    os.makedirs(os.path.dirname('../output/base/{}.txt'.format(name)), exist_ok=True)
    with open('../output/base/{}.txt'.format(name), 'w') as file:
        file.write('Benchmark results : {}\n'.format(name))

        # print analytics
        analytics_start_time, analytics_end_time = sketch.print_analytics(file)

        # calculate time
        base_time = base_end_time - base_start_time
        streaming_time = streaming_end_time - streaming_start_time
        analytics_time = analytics_end_time - analytics_start_time
        process_time = datetime.now() - process_start_time

        file.write('\nBase graph construction time: {} ({:.2f}%)\n'.format(base_time, (base_time / process_time * 100.0)))
        file.write('Streaming time: {} ({:.2f}%)\n'.format(streaming_time, (streaming_time / process_time * 100.0)))
        file.write('Analytics time: {} ({:.2f}%)\n'.format(analytics_time, (analytics_time / process_time * 100)))
        file.write('Total process time: {}\n'.format(process_time))


if __name__ == '__main__':
    sketches = [
        (FullGraph, 'FullGraph'),
        (GlobalCountMin, 'GlobalCountMin'),
        (GSketch, 'GSketch'),
        (TCM, 'TCM'),
    ]

    for sketch, name in sketches:
        test(sketch, name)
