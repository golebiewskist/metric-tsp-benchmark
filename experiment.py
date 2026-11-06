import math

from generator import generate_cities
from heldKarp import held_karp
from christofides import christofides
from metrics import measure
from theory import CalibratedTheory


def run(sizes):

    results = []

    theory = None

    for n in sizes:

        cities = generate_cities(n, seed=42)
        dist = distance_matrix(cities)

        (hk_res, hk_time, hk_mem) = measure(held_karp, dist)
        hk_cost, _ = hk_res

        (ch_res, ch_time, ch_mem) = measure(christofides, cities)
        ch_cost, _ = ch_res

        results.append({
            "n": n,
            "hk_time": hk_time,
            "hk_mem": hk_mem,
            "chr_time": ch_time,
            "chr_mem": ch_mem,
            "opt_cost": hk_cost,
            "chr_cost": ch_cost,
            "gap_%": (ch_cost - hk_cost) / hk_cost * 100
        })

        # kalibracja na pierwszym punkcie
        if theory is None:
            theory = CalibratedTheory(
                hk_ref=(n, hk_time, hk_mem),
                ch_ref=(n, ch_time, ch_mem)
            )

    return theory.enrich(results)

def distance_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = math.dist(cities[i], cities[j])

    return dist