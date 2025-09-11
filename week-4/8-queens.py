import random

def random_board(n=8):
    
    return [random.randint(0, n-1) for _ in range(n)]

def conflicts(board):
    
    n = len(board)
    cnt = 0
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j] or abs(board[i]-board[j]) == abs(i-j):
                cnt += 1
    return cnt

def best_neighbor(board):
    """Return best neighbor by moving one queen in its column."""
    n = len(board)
    best = board[:]
    best_conf = conflicts(board)
    for col in range(n):
        original_row = board[col]
        for row in range(n):
            if row != original_row:
                new_board = board[:]
                new_board[col] = row
                c = conflicts(new_board)
                if c < best_conf:
                    best = new_board
                    best_conf = c
    return best, best_conf

def hill_climb(board):
    """Perform steepest-ascent hill climbing."""
    current = board
    current_conf = conflicts(current)
    while True:
        neighbor, neighbor_conf = best_neighbor(current)
        if neighbor_conf < current_conf:
            current, current_conf = neighbor, neighbor_conf
        else:
            return current, current_conf

def restart_hill_climb(max_restarts=100, n=8):
    for _ in range(max_restarts):
        board = random_board(n)
        solution, conf = hill_climb(board)
        if conf == 0:
            return solution
    return None

if __name__ == "__main__":
    sol = restart_hill_climb()
    if sol:
        print("Solution found:", sol)
    else:
        print("No solution found")

