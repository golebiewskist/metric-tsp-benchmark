from itertools import combinations


def held_karp(dist):
    n = len(dist)

    # DP: (mask, j) -> cost
    dp = {}
    parent = {}

    # start z miasta 0
    for j in range(1, n):
        dp[(1 << j, j)] = dist[0][j]

    # wszystkie podzbiory
    for size in range(2, n):

        for subset in combinations(range(1, n), size):

            mask = 0
            for bit in subset:
                mask |= (1 << bit)

            for j in subset:
                prev_mask = mask ^ (1 << j)

                best_cost = float('inf')
                best_parent = None

                for i in subset:
                    if i == j:
                        continue

                    cost = dp[(prev_mask, i)] + dist[i][j]

                    if cost < best_cost:
                        best_cost = cost
                        best_parent = i

                dp[(mask, j)] = best_cost
                parent[(mask, j)] = best_parent

    full_mask = (1 << n) - 2  # wszystkie oprócz 0

    best_cost = float('inf')
    last = None

    for j in range(1, n):
        cost = dp[(full_mask, j)] + dist[j][0]
        if cost < best_cost:
            best_cost = cost
            last = j

    # odtwarzanie ścieżki
    path = [0]
    mask = full_mask
    node = last

    rev_path = []

    while node is not None:
        rev_path.append(node)
        prev = parent.get((mask, node))
        mask ^= (1 << node)
        node = prev

    path.extend(reversed(rev_path))
    path.append(0)

    return best_cost, path