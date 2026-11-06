import math
import heapq
from collections import defaultdict, Counter



def euclidean(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def distance_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            dist[i][j] = euclidean(cities[i], cities[j])

    return dist



def prim_mst(dist):
    n = len(dist)
    in_mst = [False]*n
    key = [float('inf')]*n
    parent = [-1]*n

    key[0] = 0

    for _ in range(n):
        u = min(
            (i for i in range(n) if not in_mst[i]),
            key=lambda i: key[i]
        )

        in_mst[u] = True

        for v in range(n):
            if not in_mst[v] and dist[u][v] < key[v]:
                key[v] = dist[u][v]
                parent[v] = u

    mst = defaultdict(list)

    for v in range(1, n):
        u = parent[v]
        mst[u].append(v)
        mst[v].append(u)

    return mst



def find_odd_vertices(mst, n):
    degree = [0]*n

    for u in mst:
        for v in mst[u]:
            degree[u] += 1

    return [i for i in range(n) if degree[i] % 2 == 1]


def greedy_matching(nodes, dist):
    used = set()
    edges = []

    nodes = sorted(nodes)

    for i in range(len(nodes)):
        if nodes[i] in used:
            continue

        best = None
        best_d = float('inf')

        for j in range(i+1, len(nodes)):
            if nodes[j] in used:
                continue

            d = dist[nodes[i]][nodes[j]]
            if d < best_d:
                best_d = d
                best = nodes[j]

        used.add(nodes[i])
        used.add(best)
        edges.append((nodes[i], best))

    return edges


def euler_tour(graph, start=0):
    graph = {u: list(vs) for u, vs in graph.items()}
    stack = [start]
    path = []

    while stack:
        v = stack[-1]

        if graph[v]:
            u = graph[v].pop()
            graph[u].remove(v)
            stack.append(u)
        else:
            path.append(stack.pop())

    return path[::-1]


def christofides(cities):
    dist = distance_matrix(cities)
    n = len(cities)

    mst = prim_mst(dist)

    odd = find_odd_vertices(mst, n)

    matching = greedy_matching(odd, dist)

    multigraph = defaultdict(list)

    for u in mst:
        for v in mst[u]:
            multigraph[u].append(v)

    for u, v in matching:
        multigraph[u].append(v)
        multigraph[v].append(u)

    tour = euler_tour(multigraph, start=0)

    # shortcut (remove repeats)
    visited = set()
    path = []

    for v in tour:
        if v not in visited:
            visited.add(v)
            path.append(v)

    path.append(path[0])

    # compute cost
    cost = 0
    for i in range(len(path)-1):
        cost += dist[path[i]][path[i+1]]

    return cost, path