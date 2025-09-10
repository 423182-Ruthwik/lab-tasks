import random
import time
from tabulate import tabulate



def graph(n, extra_edges=2000):
    graph = {}
    for i in range(n):
        graph[i] = []

   
    for i in range(1, n):
        j = random.randint(0, i - 1)
        w = random.randint(1, 10)
        graph[i].append((j, w))
        graph[j].append((i, w))

    for _ in range(extra_edges):
        u, v = random.sample(range(n), 2)
        w = random.randint(1, 10)
        graph[u].append((v, w))
        graph[v].append((u, w))


    return graph


def dfs(graph, start, goal):
    visited = set()
    stack = [(start, [start])]
    nodes_generated = 0


    while stack:
        node, path = stack.pop()
        nodes_generated += 1
        if node == goal:
            return path, nodes_generated
        if node not in visited:
            visited.add(node)
            for neighbor, _ in graph[node]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None, nodes_generated


def bfs(graph, start, goal):
    visited = set()
    queue = [(start, [start])]
    nodes_generated = 0

    while queue:
        node, path = queue.pop(0)
        nodes_generated += 1
        if node == goal:
            return path, nodes_generated
        if node not in visited:
            visited.add(node)
            for neighbor, _ in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None, nodes_generated


def ucs(graph, start, goal):
    visited = set()
    pq = [(0, start, [start])]
    nodes_generated = 0

    while pq:
        pq.sort(key=lambda x: x[0])  
        cost, node, path = pq.pop(0)
        nodes_generated += 1
        if node == goal:
            return path, nodes_generated, cost
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node]:
                pq.append((cost + weight, neighbor, path + [neighbor]))
    return None, nodes_generated, float("inf")


def ids(graph, start, goal, max_depth=50):
    def dls(node, path, depth):
        nonlocal nodes_generated
        nodes_generated += 1
        if node == goal:
            return path
        if depth == 0:
            return None
        for neighbor, _ in graph[node]:
            if neighbor not in path:
                new_path = dls(neighbor, path + [neighbor], depth - 1)
                if new_path:
                    return new_path
        return None  

    nodes_generated = 0
    for depth in range(max_depth):
        path = dls(start, [start], depth)
        if path:
            return path, nodes_generated
    return None, nodes_generated
if __name__ == "__main__":
    n = 1000
    G = graph(n)

    start, goal = random.sample(list(G.keys()), 2)
    print(f"Start: {start}, Goal: {goal}\n")

    algorithms = {
        "DFS": dfs,
        "BFS": bfs,
        "UCS": ucs,
        "IDS": ids
    }

    results = []

    for algo, func in algorithms.items():
        times = []
        nodes = []
        lengths = []
        cost = "-"

       
        for _ in range(5):
            t1 = time.time()
            if algo == "UCS":
                path, gen_nodes, c = func(G, start, goal)
                cost = c
            else:
                path, gen_nodes = func(G, start, goal)
            t2 = time.time()

            if path:
                lengths.append(len(path))
            nodes.append(gen_nodes)
            times.append(t2 - t1)

        avg_time = sum(times) / len(times)
        avg_nodes = sum(nodes) / len(nodes)
        avg_length = sum(lengths) / len(lengths) if lengths else "-"

        results.append([algo, avg_time, avg_nodes, avg_length, cost])

    print(tabulate(results, headers=["Algorithm", "Avg Time (s)", "Avg Nodes", "Avg Path Length", "Cost"]))

