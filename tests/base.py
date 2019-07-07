from _datetime import datetime

from sketches.full_graph import FullGraph
from sketches.global_countmin import GlobalCountMin
from sketches.gsketch import GSketch
from sketches.tcm import TCM


def test(sketch, name):
    process_start_time = datetime.now()

    sketch = sketch(base_path='./datasets/unicorn_wget/benign_base/',
                    streaming_path='./datasets/unicorn_wget/benign_streaming/')

    # construct base graph
    base_start_time, base_end_time = sketch.construct_base_graph()

    # streaming edges
    streaming_start_time, streaming_end_time = sketch.construct_stream_graph()

    print('')
    print('Benchmark results : {}'.format(name))
    print('')

    # print analytics
    analytics_start_time, analytics_end_time = sketch.print_analytics()

    # calculate time
    base_time = base_end_time - base_start_time
    streaming_time = streaming_end_time - streaming_start_time
    analytics_time = analytics_end_time - analytics_start_time
    process_time = datetime.now() - process_start_time

    print('')
    print('Base graph construction time: {} ({:.2f}%)'.format(base_time, (base_time / process_time * 100.0)))
    print('Streaming time: {} ({:.2f}%)'.format(streaming_time, (streaming_time / process_time * 100.0)))
    print('Analytics time: {} ({:.2f}%)'.format(analytics_time, (analytics_time / process_time * 100)))
    print('Total process time: {}'.format(process_time))


if __name__ == '__main__':
    sketches = [
        (FullGraph, 'FullGraph'),
        (GlobalCountMin, 'GlobalCountMin'),
        (GSketch, 'GSketch'),
        (TCM, 'TCM'),
    ]

    for sketch, name in sketches:
        test(sketch, name)
