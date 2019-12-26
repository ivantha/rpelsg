from tests._dc_test import dc_test
from tests._dc_visualize import dc_visualize
from tests._dd_test import dd_test
from tests._dd_visualize import dd_visualize
from tests._ewd_test import ewd_test
from tests._ewd_visualize import ewd_visualize
from tests.are_test import are_test
from tests.are_visualize import are_visualize
from tests.buildtime_test import buildtime_test
from tests.buildtime_visualize import buildtime_visualize
from tests.he_test import he_test
from tests.he_visualize import he_visualize
from tests.hn_test import hn_test
from tests.hn_visualize import hn_visualize
from tests.neq_test import neq_test
from tests.neq_visualize import neq_visualize
from tests.pickle_it import pickle_it

if __name__ == '__main__':
    datasets = [
        '../datasets/unicorn_wget/benign_base_100/',
    ]

    # pickle_it(datasets)

    # buildtime_test(datasets)
    # buildtime_visualize()

    # are_test(datasets)
    # are_visualize()

    # neq_test(datasets)
    # neq_visualize()

    # dd_test(datasets)
    # dd_visualize()

    # ewd_test(datasets)
    # ewd_visualize()

    # dc_test(datasets)
    # dc_visualize()

    hn_test(datasets)
    hn_visualize()

    he_test(datasets)
    he_visualize()
