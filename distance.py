import math

def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def distance_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            dist[i][j] = euclidean(cities[i], cities[j])

    return dist