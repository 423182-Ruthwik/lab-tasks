import random, time, tracemalloc
import sys
sys.setrecursionlimit(25000)


class CSP:
    def __init__(self, variables, domain, graph):
        self.variables = variables
        self.domain = domain
        self.graph = graph

def _planar_graph(nodes):
    edges = {(0,1),(1,2),(2,0)}
    faces = [(0,1,2)]
    neighbours = {0:[1,2], 1:[0,2], 2:[0,1]}
    
    for node in range(3, nodes):
        f = random.choice(faces)
        faces.remove(f)
        a, b, c = f
        new_edges = [(a,node),(b,node),(c,node)]
        for e in new_edges:
            edges.add(tuple(sorted(e)))
        neighbours[node] = [a,b,c]
        for u in f:
            neighbours[u].append(node)
        faces.extend([(a,b,node),(a,c,node),(b,c,node)])
    return neighbours

def backtracking(csp, solution, stats):
    if len(solution) == len(csp.variables):
        return solution
    
    stats["nodesExplored"] += 1
  
    node = next(v for v in csp.variables if v not in solution)
    
    for color in csp.domain[node]:
        if all(solution.get(neigh) != color for neigh in csp.graph[node]):
            solution[node] = color
            if backtracking(csp, solution, stats):
                return solution
            del solution[node]
    return None

def solve_csp(csp):
    stats = {"nodesExplored": 0}
    start = time.time()
    solution = backtracking(csp, {}, stats)
    stats["time"] = round(time.time() - start, 5)
    return solution, stats

print("Backtracking Graph Coloring (4-colors)")
print("Nodes | Explored | Time(s) | Memory(MB)")
print("---------------------------------------")

for n in [100, 500, 1000]:
    graph = random_planar_graph(n)
    variables = list(range(n))
    domain = {v: set(range(4)) for v in variables}

    csp = CSP(variables, domain, graph)

    tracemalloc.start()
    solution, stats = solve_csp(csp)
    _, memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"{n:<5} | {stats['nodesExplored']:<8} | {stats['time']:<7} | {memory/1024/1024:.2f}")


