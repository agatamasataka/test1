"""Console-based Othello (Reversi) game for two players."""

from typing import List, Tuple, Optional

EMPTY = "."
BLACK = "B"
WHITE = "W"
SIZE = 8

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),         (0, 1),
    (1, -1),  (1, 0), (1, 1),
]

Board = List[List[str]]


def create_board() -> Board:
    """Create initial board with starting pieces."""
    board = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
    mid = SIZE // 2
    board[mid - 1][mid - 1] = WHITE
    board[mid][mid] = WHITE
    board[mid - 1][mid] = BLACK
    board[mid][mid - 1] = BLACK
    return board


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < SIZE and 0 <= c < SIZE


def opponent(player: str) -> str:
    return BLACK if player == WHITE else WHITE


def valid_moves(board: Board, player: str) -> List[Tuple[int, int]]:
    moves = []
    opp = opponent(player)
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] != EMPTY:
                continue
            for dr, dc in directions:
                i, j = r + dr, c + dc
                has_opp_between = False
                while in_bounds(i, j) and board[i][j] == opp:
                    i += dr
                    j += dc
                    has_opp_between = True
                if has_opp_between and in_bounds(i, j) and board[i][j] == player:
                    moves.append((r, c))
                    break
    return moves


def apply_move(board: Board, player: str, r: int, c: int) -> bool:
    if (r, c) not in valid_moves(board, player):
        return False
    board[r][c] = player
    opp = opponent(player)
    for dr, dc in directions:
        i, j = r + dr, c + dc
        cells_to_flip = []
        while in_bounds(i, j) and board[i][j] == opp:
            cells_to_flip.append((i, j))
            i += dr
            j += dc
        if cells_to_flip and in_bounds(i, j) and board[i][j] == player:
            for fr, fc in cells_to_flip:
                board[fr][fc] = player
    return True


def has_valid_move(board: Board, player: str) -> bool:
    return len(valid_moves(board, player)) > 0


def game_over(board: Board) -> bool:
    return not (has_valid_move(board, BLACK) or has_valid_move(board, WHITE))


def count_pieces(board: Board) -> Tuple[int, int]:
    b = sum(row.count(BLACK) for row in board)
    w = sum(row.count(WHITE) for row in board)
    return b, w


def print_board(board: Board) -> None:
    header = "  " + " ".join(str(i + 1) for i in range(SIZE))
    print(header)
    for idx, row in enumerate(board):
        print(str(idx + 1) + " " + " ".join(row))
    b, w = count_pieces(board)
    print(f"Score -> {BLACK}: {b} {WHITE}: {w}\n")


def main() -> None:
    board = create_board()
    player = BLACK
    while not game_over(board):
        print_board(board)
        moves = valid_moves(board, player)
        if not moves:
            print(f"{player} has no valid moves, skipping turn.")
            player = opponent(player)
            continue
        move_str = input(f"{player}'s move (row col) or 'q' to quit: ")
        if move_str.lower() == "q":
            print("Game aborted.")
            return
        try:
            r_str, c_str = move_str.strip().split()
            r, c = int(r_str) - 1, int(c_str) - 1
        except ValueError:
            print("Invalid input. Please enter row and column numbers.")
            continue
        if not in_bounds(r, c) or not apply_move(board, player, r, c):
            print("Invalid move. Try again.")
            continue
        player = opponent(player)
    print_board(board)
    b, w = count_pieces(board)
    if b > w:
        print(f"{BLACK} wins!")
    elif w > b:
        print(f"{WHITE} wins!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()
