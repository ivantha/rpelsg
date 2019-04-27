from pympler import asizeof

from sketches.full_graph.graph import Graph

graph = None


def init_environment():
    global graph

    graph = Graph()


def add_node(node_id: str):
    global graph

    graph.add_node(node_id)


def add_edge(source_id: str, target_id: str):
    global graph

    assert source_id in graph._nodes, 'source_id "{}" not found'.format(source_id)
    assert target_id in graph._nodes, 'target_id "{}" not found'.format(target_id)

    graph.add_edge(source_id, target_id)


def print_analytics():
    global graph

    print('Node count: {:,}'.format(graph._node_count))
    print('Edge count: {:,}'.format(graph._edge_count))
    print('Graph object size: {} bytes ({:.4f} MB)'.format(asizeof.asizeof(graph),
                                                           asizeof.asizeof(graph) / 1024.0 / 1024.0))
