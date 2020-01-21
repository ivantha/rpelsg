import itertools
import random
from typing import List


# reservoir sampling
def select_k_items(items: List, k: int):
    i = 0
    reservoir = [0] * k

    for item in items:
        if i < k:
            reservoir[i] = item
        else:
            j = random.randrange(i + 1)
            if j < k:
                reservoir[j] = item

        i += 1

    return reservoir


# reservoir sampling from multiple lists
def select_k_items_from_lists(items: List, k: int):
    i = 0
    reservoir = [0] * k

    for item in itertools.chain(*items):
        if i < k:
            reservoir[i] = item
        else:
            j = random.randrange(i + 1)
            if j < k:
                reservoir[j] = item

        i += 1

    return reservoir