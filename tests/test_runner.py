import multiprocessing

from tests.are_test import are_test
from tests.are_visualize import are_visualize
from tests.buildtime_test import buildtime_test
from tests.buildtime_visualize import buildtime_visualize
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
from tests.neq_test import neq_test
from tests.neq_visualize import neq_visualize

if __name__ == '__main__':
    datasets = [
        '../datasets/unicorn_wget/benign_base_10/',
    ]

    def run_test(funs):
        test_fun, visualize_fun = funs[0], funs[1]
        test_fun(datasets)
        visualize_fun()


    pool = multiprocessing.Pool()
    pool.map(run_test, [
        [buildtime_test, buildtime_visualize],
        [are_test, are_visualize],
        [neq_test, neq_visualize],
        [dd_test, dd_visualize],
        [ewd_test, ewd_visualize],
        [dc_test, dc_visualize],
        [hn_test, hn_visualize],
        [he_test, he_visualize],
    ])
    pool.close()
