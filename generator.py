import random

def generate_cities(n, max_coord=1000, seed=None):
    if seed is not None:
        random.seed(seed)

    return [
        (random.uniform(0, max_coord), random.uniform(0, max_coord))
        for _ in range(n)
    ]