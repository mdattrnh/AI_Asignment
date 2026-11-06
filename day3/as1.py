#BFS
from collections import deque
def bfs(graph, start, goal):
    fringe = deque([(start, [start], 0)])
    discovered = {start}
    order = []
    while fringe:
        node, path, cost = fringe.popleft()
        order.append(node)
        if node == goal:
            return path, cost, order
        for neighbor, weight in graph.get(node, []):
            if neighbor not in discovered:
                discovered.add(neighbor)
                fringe.append((
                    neighbor,
                    path + [neighbor],
                    cost + weight
                ))
    return None, None, order
#DFS 
def dfs(graph, start, goal):
    fringe = [(start, [start], 0)]
    order = []
    while fringe:
        node, path, cost = fringe.pop()
        order.append(node)
        if node == goal:
            return path, cost, order
        for neighbor, weight in reversed(graph.get(node, [])):
            if neighbor not in path:
                fringe.append((
                    neighbor,
                    path + [neighbor],
                    cost + weight
                ))
    return None, None, order
#UCS
from heapq import heappop, heappush
from itertools import count
def ucs(graph, start, goal):
    tie_breaker = count()
    fringe = [(0, next(tie_breaker), start, [start])]
    best_cost = {start: 0}
    order = []

    while fringe:
        cost, _, node, path = heappop(fringe)

        if cost != best_cost.get(node):
            continue

        order.append(node)

        if node == goal:
            return path, cost, order

        for neighbor, weight in graph.get(node, []):
            if weight < 0:
                raise ValueError("Trọng số phải không âm")

            new_cost = cost + weight

            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                heappush(fringe, (
                    new_cost,
                    next(tie_breaker),
                    neighbor,
                    path + [neighbor]
                ))

    return None, None, order
#DLS

def dls(graph, start, goal, limit):
    if limit < 0:
        raise ValueError("Giới hạn độ sâu phải >= 0")

    fringe = [(start, [start], 0, 0)]
    order = []

    while fringe:
        node, path, cost, depth = fringe.pop()
        order.append(node)

        if node == goal:
            return path, cost, order

        if depth == limit:
            continue

        for neighbor, weight in reversed(graph.get(node, [])):
            if neighbor not in path:
                fringe.append((
                    neighbor,
                    path + [neighbor],
                    cost + weight,
                    depth + 1
                ))

    return None, None, order
#IDS
def ids(graph, start, goal, max_depth=None):
    if max_depth is None:
        vertices = {start, goal} | set(graph)

        vertices.update(
            v
            for edges in graph.values()
            for v, _ in edges
        )
        max_depth = len(vertices) - 1

    history = []

    for limit in range(max_depth + 1):
        path, cost, order = dls(
            graph, start, goal, limit
        )

        history.append((limit, order))

        if path is not None:
            return path, cost, history

    return None, None, history
#
