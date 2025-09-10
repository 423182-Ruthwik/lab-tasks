import random

GOAL = [1,2,3,4,5,6,7,8,0]  # 0 = blank

def manhattan(state):
    """Heuristic: total Manhattan distance."""
    dist = 0
    for i, val in enumerate(state):
        if val == 0: continue
        goal_pos = GOAL.index(val)
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(goal_pos, 3)
        dist += abs(x1-x2) + abs(y1-y2)
    return dist

def neighbors(state):
    """Generate possible states by sliding blank."""
    res = []
    i = state.index(0)
    x, y = divmod(i, 3)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    for dx,dy in moves:
        nx, ny = x+dx, y+dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            j = nx*3 + ny
            new = state[:]
            new[i], new[j] = new[j], new[i]
            res.append(new)
    return res

def hill_climb(state, max_steps=1000):
    current = state
    current_h = manhattan(current)
    for _ in range(max_steps):
        neighs = neighbors(current)
        best = min(neighs, key=manhattan)
        best_h = manhattan(best)
        if best_h < current_h:
            current, current_h = best, best_h
        else:
            break
    return current, current_h

def random_restart_hill_climb(max_restarts=50):
    best_state, best_h = None, float("inf")
    for _ in range(max_restarts):
        state = random.sample(range(9), 9)
        sol, h = hill_climb(state)
        if h < best_h:
            best_state, best_h = sol, h
        if h == 0:
            return sol
    return best_state

if __name__ == "__main__":
    sol = random_restart_hill_climb()
    print("Result:", sol, "Heuristic:", manhattan(sol))

