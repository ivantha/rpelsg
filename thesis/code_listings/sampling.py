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