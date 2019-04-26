from _datetime import datetime

from data_processor import *
from solutions import full_graph

if __name__ == '__main__':
    process_start_time = datetime.now()

    full_graph.init_environment()

    # base graph
    base_start_time = datetime.now()
    base_data_files = get_files('./datasets/unicorn_wget/benign_base/')
    for data_file in base_data_files:
        for line in get_lines(data_file):
            source_id, target_id, _ = line.split()

            full_graph.add_node(source_id)
            full_graph.add_node(target_id)
            full_graph.add_edge(source_id, target_id)
    base_end_time = datetime.now()

    # streaming graph
    streaming_start_time = datetime.now()
    streaming_data_files = get_files('./datasets/unicorn_wget/benign_streaming/')
    for data_file in streaming_data_files:
        for line in get_lines(data_file):
            source_id, target_id, _ = line.split()

            full_graph.add_node(source_id)
            full_graph.add_node(target_id)
            full_graph.add_edge(source_id, target_id)
    streaming_end_time = datetime.now()

    # print analytics
    analytics_start_time = datetime.now()
    full_graph.print_analytics()
    analytics_end_time = datetime.now()

    print('')
    base_time = base_end_time - base_start_time
    streaming_time = streaming_end_time - streaming_start_time
    analytics_time = analytics_end_time - analytics_start_time
    process_time = datetime.now() - process_start_time
    print('Base time: {} ({:.2f}%)'.format(base_time, (base_time / process_time * 100.0)))
    print('Streaming time: {} ({:.2f}%)'.format(streaming_time, (streaming_time / process_time * 100.0)))
    print('Analytics time: {} ({:.2f}%)'.format(analytics_time, (analytics_time / process_time * 100)))
    print('Process time: {}'.format(process_time))