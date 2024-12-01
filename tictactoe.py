import argparse
import random

PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "

def is_full(board):
    return all(cell != EMPTY for cell in board)

def check_winner(board):
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6],             # Diagonals
    ]
    for positions in win_positions:
        values = [board[i] for i in positions]
        if values[0] != EMPTY and values[0] == values[1] == values[2]:
            return values[0]
    return None

def get_possible_moves(board):
    return [i for i in range(9) if board[i] == EMPTY]

def evaluate_state(board, current_player):
    winner = check_winner(board)
    if winner == PLAYER_X:
        return 1  # X wins
    elif winner == PLAYER_O:
        return -1  # O wins
    elif is_full(board):
        return 0  # Draw
    else:
        next_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O
        possible_moves = get_possible_moves(board)
        scores = []
        for move in possible_moves:
            new_board = board[:]
            new_board[move] = current_player
            scores.append(evaluate_state(new_board, next_player))
        return max(scores) if current_player == PLAYER_X else min(scores)

def make_bi_move(board, current_player):
    possible_moves = get_possible_moves(board)
    next_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O
    move_scores = {}
    
    for move in possible_moves:
        new_board = board[:]
        new_board[move] = current_player
        move_scores[move] = evaluate_state(new_board, next_player)
    
    if current_player == PLAYER_X:
        best_score = max(move_scores.values())
    else:
        best_score = min(move_scores.values())
    best_moves = [move for move, score in move_scores.items() if score == best_score]
    return random.choice(best_moves)  # Return one of the optimal moves

def play_game(mode):
    board = [EMPTY] * 9
    current_player = PLAYER_X
    while check_winner(board) is None and not is_full(board):
        if mode == current_player:
            print("Current Board:")
            for i in range(0, 9, 3):
                print(board[i:i+3])
            valid_move = False
            while not valid_move:
                move = int(input(f"Enter move for {current_player}: ")) - 1
                if board[move] == EMPTY:
                    valid_move = True
                else:
                    print("Invalid move, board position already filled, try again:")
        else:
            move = make_bi_move(board, current_player)
        board[move] = current_player
        current_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O
    winner = check_winner(board)
    return board, winner

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="Mode for simulation, sim for two agents, X to play as X, O to play as O")
    args = parser.parse_args()
    mode = args.mode
    if mode == None:
        mode = "sim"

    if mode not in ["sim", PLAYER_X, PLAYER_O]:
        print("Invalid mode, valid modes are sim, X, O")
        exit()

    if mode != "sim":
        print("When prompted enter moves from 1 to 9, board positions are as follows")
        print("['1', '2', '3']")
        print("['4', '5', '6']")
        print("['7', '8', '9']")
    
    board, winner = play_game(mode)
    print("Final Board:")
    for i in range(0, 9, 3):
        print(board[i:i+3])
    if winner:
        print(f"Winner: {winner}")
    else:
        print("Result: Draw")
