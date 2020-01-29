import multiprocessing

from common.utils import get_edges_in_path
from tests.are_test import are_test
from tests.are_visualize import are_visualize
from tests.buildtime_test import buildtime_test
from tests.buildtime_visualize import buildtime_visualize
from tests.clust_test import clust_test
from tests.clust_visualize import clust_visualize
from tests.dc_test import dc_test
from tests.dc_visualize import dc_visualize
from tests.dd_test import dd_test
from tests.dd_visualize import dd_visualize
from tests.ewd_test import ewd_test
from tests.ewd_visualize import ewd_visualize
from tests.he_test import he_test
from tests.he_visualize import he_visualize
from tests.hn_test import hn_test
from tests.hn_visualize import hn_visualize
from tests.insertionrate1_test import insertionrate1_test
from tests.insertionrate1_visualize import insertionrate1_visualize
from tests.insertionrate2_test import insertionrate2_test
from tests.insertionrate2_visualize import insertionrate2_visualize
from tests.neq_test import neq_test
from tests.neq_visualize import neq_visualize
from tests.pagerank_test import pagerank_test
from tests.pagerank_visualize import pagerank_visualize
from tests.smallworld_test import smallworld_test
from tests.smallworld_visualize import smallworld_visualize

if __name__ == '__main__':
    datasets = [
        '../datasets/unicorn-wget/benign_base_10/',
    ]

    # analyze datasets
    for dataset in datasets:
        print('Analyzing : {}'.format(dataset))
        edges = get_edges_in_path(dataset)
        print('# edges : {:,}'.format(len(edges)))
        nodes = set([edge[0] for edge in edges] + [edge[1] for edge in edges])
        print('# nodes : {:,}'.format(len(nodes)))

    def run_test(funs):
        test_fun = funs[0]
        test_fun(datasets)

        # run visualize_funs (if there are any)
        if len(funs) > 1:
            for i in range(1, len(funs)):
                funs[i]()

    pool = multiprocessing.Pool()
    pool.map(run_test, [
        # [buildtime_test, buildtime_visualize],
        # [insertionrate1_test, insertionrate1_visualize],
        # [insertionrate2_test, insertionrate2_visualize],

        [are_test, are_visualize],
        [neq_test, neq_visualize],

        # [dd_test, dd_visualize],
        # [ewd_test, ewd_visualize],

        # [dc_test, dc_visualize],

        # [hn_test, hn_visualize],
        # [he_test, he_visualize],

        # [clust_test, clust_visualize],
        # [smallworld_test, smallworld_visualize],
        # [pagerank_test, pagerank_visualize]
    ])
    pool.close()
