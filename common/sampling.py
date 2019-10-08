import random

from common import utils


# Reservoir sampling
def select_k_items(path: str, k: int):
    i = 0
    reservoir = [0] * k

    for data_file in utils.get_txt_files(path):
        with open(data_file) as file:
            for line in file.readlines():
                source_id, target_id = line.strip().split(',')

                if i < k:
                    reservoir[i] = (source_id, target_id)
                else:
                    j = random.randrange(i + 1)
                    if j < k:
                        reservoir[j] = (source_id, target_id)

                i += 1

    return reservoir
