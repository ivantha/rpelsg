import random
from typing import List


# Reservoir sampling
def select_k_items(edges: List, k: int):
    i = 0
    reservoir = [0] * k

    for edge in edges:
        if i < k:
            reservoir[i] = edge
        else:
            j = random.randrange(i + 1)
            if j < k:
                reservoir[j] = edge

        i += 1

    return reservoir
