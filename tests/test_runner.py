from tests.are_test import are_test
from tests.are_visualize import are_visualize
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
from tests.sketch_time_test import sketch_time_test
from tests.sketch_time_visualize import sketch_time_visualize

if __name__ == '__main__':
    sketch_time_test(
        '../datasets/unicorn_wget_small/benign_base/',
        '../datasets/unicorn_wget_small/benign_streaming/'
    )
    sketch_time_visualize()

    are_test(
        '../datasets/unicorn_wget_small/benign_base/',
        '../datasets/unicorn_wget_small/benign_streaming/'
    )
    are_visualize()

    neq_test(
        '../datasets/unicorn_wget_small/benign_base/',
        '../datasets/unicorn_wget_small/benign_streaming/'
    )
    neq_visualize()

    dd_test(
        '../datasets/unicorn_wget_small/benign_base/',
        '../datasets/unicorn_wget_small/benign_streaming/'
    )
    dd_visualize()

    ewd_test(
        '../datasets/unicorn_wget_small/benign_base/',
        '../datasets/unicorn_wget_small/benign_streaming/'
    )
    ewd_visualize()

    hn_test(
        '../datasets/unicorn_wget_small/benign_base/',
        '../datasets/unicorn_wget_small/benign_streaming/'
    )
    hn_visualize()

    he_test(
        '../datasets/unicorn_wget_small/benign_base/',
        '../datasets/unicorn_wget_small/benign_streaming/'
    )
    he_visualize()
