import heapq

# Helper class for representing the state of the puzzle
class PuzzleState:
    def _init_(self, tiles, blank_index=None, parent=None, move=None, depth=0):
        self.tiles = tiles
        self.blank_index = blank_index if blank_index is not None else tiles.index(0)
        self.parent = parent
        self.move = move
        self.depth = depth
        self.size = int(len(tiles) ** 0.5)

    def get_neighbors(self):
        neighbors = []
        blank_row, blank_col = divmod(self.blank_index, self.size)

        def swap_and_create(new_blank_index):
            new_tiles = self.tiles[:]
            new_tiles[self.blank_index], new_tiles[new_blank_index] = new_tiles[new_blank_index], new_tiles[self.blank_index]
            neighbors.append(PuzzleState(new_tiles, new_blank_index, self, new_blank_index, self.depth + 1))

        if blank_row > 0:  # Up
            swap_and_create(self.blank_index - self.size)
        if blank_row < self.size - 1:  # Down
            swap_and_create(self.blank_index + self.size)
        if blank_col > 0:  # Left
            swap_and_create(self.blank_index - 1)
        if blank_col < self.size - 1:  # Right
            swap_and_create(self.blank_index + 1)

        return neighbors

    def is_goal(self, goal_state):
        return self.tiles == goal_state.tiles

    def _eq_(self, other):
        return isinstance(other, PuzzleState) and self.tiles == other.tiles

    def _hash_(self):
        return hash(tuple(self.tiles))

# IDS (Iterative Deepening Search) implementation
def iterative_deepening_search(initial_state, goal_state):
    def depth_limited_search(state, goal_state, limit):
        if state.is_goal(goal_state):
            return state
        elif limit == 0:
            return None
        else:
            for neighbor in state.get_neighbors():
                result = depth_limited_search(neighbor, goal_state, limit - 1)
                if result is not None:
                    return result
        return None

    depth = 0
    while True:
        result = depth_limited_search(initial_state, goal_state, depth)
        if result is not None:
            return result
        depth += 1

# UCS (Uniform Cost Search) implementation
class PrioritizedItem:
    def _init_(self, priority, item):
        self.priority = priority
        self.item = item

    def _lt_(self, other):
        return self.priority < other.priority

def uniform_cost_search_fixed(initial_state, goal_state):
    frontier = [PrioritizedItem(0, initial_state)]
    explored = set()
    state_costs = {initial_state: 0}

    while frontier:
        current_node = heapq.heappop(frontier)
        current_state = current_node.item
        cost = current_node.priority

        if current_state.is_goal(goal_state):
            return current_state

        explored.add(current_state)

        for neighbor in current_state.get_neighbors():
            new_cost = cost + 1  # Each move has a cost of 1
            if neighbor not in explored or new_cost < state_costs.get(neighbor, float('inf')):
                state_costs[neighbor] = new_cost
                heapq.heappush(frontier, PrioritizedItem(new_cost, neighbor))

    return None

# Function to reconstruct the path from the goal state to the initial state
def reconstruct_path(state):
    path = []
    while state is not None:
        path.append(state.tiles)
        state = state.parent
    return path[::-1]

# Define the initial and goal states
initial_state = PuzzleState([1, 2, 3, 4, 0, 5, 6, 7, 8])
goal_state = PuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0])

# Perform Iterative Deepening Search
ids_solution = iterative_deepening_search(initial_state, goal_state)
ids_solution_path = reconstruct_path(ids_solution)

# Perform Uniform Cost Search
ucs_solution_fixed = uniform_cost_search_fixed(initial_state, goal_state)
ucs_solution_path_fixed = reconstruct_path(ucs_solution_fixed)

# Output the solution paths
print("IDS Solution Path:")
for step in ids_solution_path:
    print(step)

print("\nUCS Solution Path:")
for step in ucs_solution_path_fixed:
    print(step)
