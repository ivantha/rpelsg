from _datetime import datetime

from sketches import full_graph

if __name__ == '__main__':
    process_start_time = datetime.now()

    sketch = full_graph

    sketch.init_environment(base_dir_path='./datasets/unicorn_wget/benign_base/',
                            streaming_dir_path='./datasets/unicorn_wget/benign_streaming/')

    # construct base graph
    base_start_time, base_end_time = sketch.construct_base_graph()

    # streaming edges
    streaming_start_time, streaming_end_time = sketch.stream_edges()

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
    print('Post analytics time: {} ({:.2f}%)'.format(analytics_time, (analytics_time / process_time * 100)))
    print('Total process time: {}'.format(process_time))
