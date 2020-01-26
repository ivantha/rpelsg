from math import sqrt

from common.globals import INT_SIZE


def print_gsketch_sizes(d):
    for i in [100, 200, 300, 400, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]:
        x = i / 2.0 / d
        x_round = round(x)
        revert = x_round * INT_SIZE * d
        print('{} : {} >> {}KB ({}MB)'.format(i, x_round, revert, revert / 1024.0))


def print_tcm_sizes(d):
    for i in [100, 200, 300, 400, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]:
        x = round(sqrt(i / (INT_SIZE * d) * 1024.0))
        print('{} : {} >> {}KB ({}MB)'.format(i, x, (x ** 2) * (INT_SIZE * d) / 1024.0, (x ** 2) * (INT_SIZE * d) / 1024.0 / 1024.0))


def print_alpha_sizes():
    for i in [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]:
        print('{} ----------------'.format(i))
        x = round(sqrt(i * 0.75 / 16.0 * 1024.0))
        print('Partitioned : {} >> {}KB ({}MB)'.format(x, (x ** 2) * 16.0 / 1024.0, (x ** 2) * 16.0 / 1024.0 / 1024.0))
        y = round(sqrt(i * 0.25 / 16.0 * 1024.0))
        print('Outliers : {} >> {}KB ({}MB)'.format(y, (y ** 2) * 16.0 / 1024.0, (y ** 2) * 16.0 / 1024.0 / 1024.0))


if __name__ == '__main__':
    print('gSketch')
    print_gsketch_sizes(7)

    print('TCM')
    print_tcm_sizes(7)