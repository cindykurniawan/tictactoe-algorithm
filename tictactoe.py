import time
from collections import deque

# =========================
# GLOBAL COUNTERS
# =========================
def reset_nodes():
    global node_minimax, node_greedy, node_bfs, node_dfs, node_brute
    node_minimax = node_greedy = node_bfs = node_dfs = node_brute = 0

# =========================
# UTIL FUNCTIONS
# =========================
def check_winner(board):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for w in wins:
        if board[w[0]] == board[w[1]] == board[w[2]] != 0:
            return board[w[0]]
    return 0

def get_moves(board):
    return [i for i in range(9) if board[i] == 0]

# =========================
# ALGORITMA
# =========================
def minimax(board, player):
    global node_minimax
    node_minimax += 1
    winner = check_winner(board)
    if winner != 0: return winner * player
    moves = get_moves(board)
    if not moves: return 0
    best = -2
    for move in moves:
        board[move] = player
        score = -minimax(board, -player)
        board[move] = 0
        if score > best: best = score
    return best

def best_move_minimax(board, player):
    best_score = -2; move_choice = None
    for move in get_moves(board):
        board[move] = player
        score = -minimax(board, -player)
        board[move] = 0
        if score > best_score: best_score = score; move_choice = move
    return move_choice

def greedy_move(board, player):
    global node_greedy
    for move in get_moves(board):
        node_greedy += 1
        board[move] = player
        winner = check_winner(board)
        board[move] = 0
        if winner == player: return move
    return get_moves(board)[0]

def bfs_move(board, player):
    global node_bfs
    queue = deque([(board, None)])
    while queue:
        node_bfs += 1
        current, first_move = queue.popleft()
        if check_winner(current) == player: return first_move
        for move in get_moves(current):
            new_board = current[:]
            new_board[move] = player
            queue.append((new_board, move if first_move is None else first_move))
    return get_moves(board)[0]

def dfs_search(board, player):
    global node_dfs
    node_dfs += 1
    if check_winner(board) != 0: return check_winner(board)
    for move in get_moves(board):
        board[move] = player
        if dfs_search(board, -player) == player:
            board[move] = 0; return player
        board[move] = 0
    return 0

def dfs_move(board, player):
    for move in get_moves(board):
        board[move] = player
        if dfs_search(board, -player) == player:
            board[move] = 0; return move
        board[move] = 0
    return get_moves(board)[0]

def brute_force(board, player):
    global node_brute
    node_brute += 1
    winner = check_winner(board)
    if winner != 0: return winner
    moves = get_moves(board)
    if not moves: return 0
    results = [brute_force(board[:i]+[player]+board[i+1:], -player) for i in moves]
    return max(results) if player == 1 else min(results)

def brute_move(board, player):
    return max(get_moves(board), key=lambda m: brute_force(board[:m]+[player]+board[m+1:], -player))

# =========================
# RUNNER
# =========================
def run_experiment():
    algos = [("Minimax", best_move_minimax), ("Greedy", greedy_move), 
             ("BFS", bfs_move), ("DFS", dfs_move), ("Brute", brute_move)]
    
    print(f"{'Algoritma':<10} | {'Node':<10} | {'Waktu (ms)':<10}")
    print("-" * 35)
    
    for name, func in algos:
        reset_nodes()
        board = [0]*9
        start = time.time()
        # Simulasi singkat untuk mengambil data node
        func(board, 1) 
        end = time.time()
        
        # Mengambil nilai node yang terupdate
        val = globals()[f"node_{name.lower() if name != 'Brute' else 'brute'}"]
        print(f"{name:<10} | {val:<10} | {(end-start)*1000:.4f}")

if __name__ == "__main__":
    run_experiment()