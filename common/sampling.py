import random

from common.utils import get_txt_files, get_lines


# Reservoir sampling
def select_k_items(path: str, k: int):
    i = 0
    reservoir = [0] * k

    data_files = get_txt_files(path)
    for data_file in data_files:
        for line in get_lines(data_file):
            source_id, target_id = line.strip().split(',')

            if i < k:
                reservoir[i] = (source_id, target_id)
            else:
                j = random.randrange(i + 1)
                if j < k:
                    reservoir[j] = (source_id, target_id)

            i += 1

    return reservoir
