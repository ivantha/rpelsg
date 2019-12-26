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
    PRIMARY_DATASET = '../datasets/unicorn_wget/benign_base_50/'

    pickle_it(
        PRIMARY_DATASET,
    )

    buildtime_test(
        PRIMARY_DATASET,
    )
    buildtime_visualize()

    # are_test(
    #     '../datasets/unicorn_wget_small/benign_base/',
    # )
    # are_visualize()

    # neq_test(
    #     '../datasets/unicorn_wget_small/benign_base/',
    # )
    # neq_visualize()

    # dd_test(
    #     '../datasets/unicorn_wget_small/benign_base/',
    # )
    # dd_visualize()

    # ewd_test(
    #     '../datasets/unicorn_wget_small/benign_base/',
    # )
    # ewd_visualize()

    # hn_test(
    #     '../datasets/unicorn_wget_small/benign_base/',
    # )
    # hn_visualize()

    # he_test(
    #     '../datasets/unicorn_wget_small/benign_base/',
    # )
    # he_visualize()
