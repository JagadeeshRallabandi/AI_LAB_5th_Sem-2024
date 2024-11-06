import random


def print_board(board):
    for i in range(3):
        print(" ".join(board[i * 3:(i + 1) * 3]))
    print()


def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    if ' ' not in board:
        return -1
    return None


def minimax(board, depth, is_maximizing):
    result = check_winner(board)
    if result is not None:
        return 10 if result == 'X' else -10 if result == 'O' else 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score


def get_best_move(board):
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move


def play_game():
    board = [' ' for _ in range(9)]
    print_board(board)

    while True:
        print("Computer's turn (X):")
        computer_move = get_best_move(board)
        board[computer_move] = 'X'
        print_board(board)

        winner = check_winner(board)
        if winner is not None:
            if winner == -1:
                print("It's a draw!")
            else:
                print(f"Player {winner} wins!")
            break

        player_move = int(input("Enter your move (0-8): "))
        while board[player_move] != ' ':
            player_move = int(input("Invalid move. Try again: "))

        board[player_move] = 'O'
        print_board(board)

        winner = check_winner(board)
        if winner is not None:
            if winner == -1:
                print("It's a draw!")
            else:
                print(f"Player {winner} wins!")
            break


if __name__ == "__main__":
    play_game()
