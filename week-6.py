import time
import copy

# Sample Sudoku puzzle (0 means empty cell)
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Helper function: check if value is valid at (row, col)
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row//3), 3 * (col//3)
    for i in range(3):
        for j in range(3):
            if board[start_row+i][start_col+j] == num:
                return False
    return True

# Find empty cell
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

# Backtracking Sudoku solver without heuristics
def solve_sudoku_bt(board, stats):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    stats['nodes'] += 1
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku_bt(board, stats):
                return True
            board[row][col] = 0  # backtrack
    return False

# Backtracking Sudoku solver with MRV heuristic
def select_mrv_cell(board):
    min_options = 10
    best_cell = None
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                options = sum(is_valid(board, i, j, num) for num in range(1,10))
                if options < min_options:
                    min_options = options
                    best_cell = (i, j)
                    if min_options == 1:
                        return best_cell
    return best_cell

def solve_sudoku_bt_mrv(board, stats):
    empty = select_mrv_cell(board)
    if not empty:
        return True
    row, col = empty
    stats['nodes'] += 1
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku_bt_mrv(board, stats):
                return True
            board[row][col] = 0
    return False

# Function to print Sudoku board
def print_board(board):
    for i in range(9):
        print(board[i])

# Function to solve and compare time and space
def compare_solvers(board):
    # Backtracking without heuristic
    board1 = copy.deepcopy(board)
    stats1 = {'nodes': 0}
    start1 = time.time()
    solve_sudoku_bt(board1, stats1)
    end1 = time.time()
    
    # Backtracking with MRV heuristic
    board2 = copy.deepcopy(board)
    stats2 = {'nodes': 0}
    start2 = time.time()
    solve_sudoku_bt_mrv(board2, stats2)
    end2 = time.time()
    
    print("Solved Sudoku (BT without heuristic):")
    print_board(board1)
    print(f"Nodes explored: {stats1['nodes']}, Time: {end1-start1:.6f} s")
    print("\nSolved Sudoku (BT with MRV heuristic):")
    print_board(board2)
    print(f"Nodes explored: {stats2['nodes']}, Time: {end2-start2:.6f} s")
    
compare_solvers(sudoku_board)

