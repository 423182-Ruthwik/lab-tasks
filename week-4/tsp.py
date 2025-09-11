import random, math

def distance(city1, city2):
    return math.hypot(city1[0]-city2[0], city1[1]-city2[1])

def total_distance(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[(i+1)%len(tour)]]) for i in range(len(tour)))

def two_opt(tour):
    """Generate neighbors using 2-opt swaps."""
    n = len(tour)
    for i in range(n-1):
        for j in range(i+2, n):
            if j-i == 1: continue
            new_tour = tour[:]
            new_tour[i:j] = reversed(new_tour[i:j])
            yield new_tour

def hill_climb(tour, cities, max_steps=500):
    current = tour
    current_cost = total_distance(current, cities)
    improved = True
    while improved:
        improved = False
        for neighbor in two_opt(current):
            cost = total_distance(neighbor, cities)
            if cost < current_cost:
                current, current_cost = neighbor, cost
                improved = True
                break
    return current, current_cost

def restart_hill_climb(cities, max_restarts=20):
    best_tour, best_cost = None, float("inf")
    n = len(cities)
    for _ in range(max_restarts):
        tour = list(range(n))
        random.shuffle(tour)
        sol, cost = hill_climb(tour, cities)
        if cost < best_cost:
            best_tour, best_cost = sol, cost
    return best_tour, best_cost

if __name__ == "__main__":
   
    cities = [(random.randint(0,100), random.randint(0,100)) for _ in range(10)]
    tour, cost = restart_hill_climb(cities)
    print("Best tour:", tour)
    print("Tour cost:", cost)

