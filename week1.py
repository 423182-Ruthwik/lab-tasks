import heapq

class PuzzleState:
    def _init_(self, board, moves=0, previous=None):
        self.board = board
        self.moves = moves
        self.previous = previous
        self.priority = self.moves + self.manhattan()

    def _lt_(self, other):
        return self.priority < other.priority

    def manhattan(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    continue
                x, y = divmod(self.board[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
        return distance

    def is_goal(self):
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def get_neighbors(self):
        neighbors = []
        x, y = next((i, j) for i, row in enumerate(self.board) for j, val in enumerate(row) if val == 0)
        directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for dx, dy in directions:
            if 0 <= dx < 3 and 0 <= dy < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[dx][dy] = new_board[dx][dy], new_board[x][y]
                neighbors.append(PuzzleState(new_board, self.moves + 1, self))
        return neighbors

    def _str_(self):
        return "\n".join(" ".join(map(str, row)) for row in self.board) + "\n"

def solve_puzzle(initial_board):
    open_set = []
    closed_set = set()
    start_state = PuzzleState(initial_board)
    heapq.heappush(open_set, start_state)

    while open_set:
        current_state = heapq.heappop(open_set)

        if current_state.is_goal():
            return current_state

        closed_set.add(tuple(map(tuple, current_state.board)))

        for neighbor in current_state.get_neighbors():
            if tuple(map(tuple, neighbor.board)) in closed_set:
                continue
            heapq.heappush(open_set, neighbor)

    return None

def print_solution(solution):
    if solution is None:
        print("No solution found!")
    else:
        path = []
        current = solution
        while current:
            path.append(current)
            current = current.previous
        path.reverse()

        for step in path:
            print(step)
            print("-" * 10)

if __name__ == "__main__":
    initial_board = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]

    solution = solve_puzzle(initial_board)
    print_solution(solution)
