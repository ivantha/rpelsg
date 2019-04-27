from _datetime import datetime

from utils import *
from sketches import full_graph

if __name__ == '__main__':
    process_start_time = datetime.now()

    sketch = full_graph

    sketch.init_environment()

    # base graph
    base_start_time = datetime.now()
    base_data_files = get_files('./datasets/unicorn_wget/benign_base/')
    for data_file in base_data_files:
        for line in get_lines(data_file):
            source_id, target_id, _ = line.split()

            sketch.add_node(source_id)
            sketch.add_node(target_id)
            sketch.add_edge(source_id, target_id)
    base_end_time = datetime.now()

    # streaming graph
    streaming_start_time = datetime.now()
    streaming_data_files = get_files('./datasets/unicorn_wget/benign_streaming/')
    for data_file in streaming_data_files:
        for line in get_lines(data_file):
            source_id, target_id, _ = line.split()

            sketch.add_node(source_id)
            sketch.add_node(target_id)
            sketch.add_edge(source_id, target_id)
    streaming_end_time = datetime.now()

    # print analytics
    analytics_start_time = datetime.now()
    sketch.print_analytics()
    analytics_end_time = datetime.now()

    # calculate time
    base_time = base_end_time - base_start_time
    streaming_time = streaming_end_time - streaming_start_time
    analytics_time = analytics_end_time - analytics_start_time
    process_time = datetime.now() - process_start_time

    print('')
    print('Base graph construction time: {} ({:.2f}%)'.format(base_time, (base_time / process_time * 100.0)))
    print('Streaming time: {} ({:.2f}%)'.format(streaming_time, (streaming_time / process_time * 100.0)))
    print('Post analytics time: {} ({:.2f}%)'.format(analytics_time, (analytics_time / process_time * 100)))
    print('Total process time: {}'.format(process_time))