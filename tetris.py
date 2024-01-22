import random
import curses

def draw_board(stdscr, board):
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            stdscr.addch(i, j * 2, cell)
    stdscr.refresh()

def clear_line(board, line):
    for i in range(line, 0, -1):
        board[i] = board[i - 1]
    board[0] = [' '] * BOARD_WIDTH

def collide(board, piece, offset):
    for i, row in enumerate(piece):
        for j, cell in enumerate(row):
            if cell == 'X' and board[i + offset[0]][j + offset[1]] != ' ':
                return True
    return False

def merge(board, piece, offset):
    for i, row in enumerate(piece):
        for j, cell in enumerate(row):
            if cell == 'X':
                board[i + offset[0]][j + offset[1]] = 'X'

def rotate(piece):
    return list(zip(*reversed(piece)))

def get_random_piece():
    pieces = [
        [['X', 'X', 'X', 'X']],
        [['X', 'X'], ['X', 'X']],
        [['X', 'X', ' '], [' ', 'X', 'X']],
        [[' ', 'X', 'X'], ['X', 'X', ' ']],
        [['X', 'X', 'X'], ['X', ' ', ' ']],
        [['X', 'X', 'X'], [' ', ' ', 'X']],
        [['X', 'X', 'X'], [' ', 'X', ' ']],
    ]
    return random.choice(pieces)

def main(stdscr):
    global BOARD_HEIGHT, BOARD_WIDTH
    BOARD_HEIGHT, BOARD_WIDTH = 20, 10

    curses.curs_set(0)
    stdscr.timeout(100)
    stdscr.keypad(1)

    board = [[' ' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    piece = get_random_piece()
    piece_offset = [0, BOARD_WIDTH // 2 - len(piece[0]) // 2]

    while True:
        new_piece_offset = [piece_offset[0] + 1, piece_offset[1]]

        if not collide(board, piece, new_piece_offset):
            piece_offset = new_piece_offset
        else:
            merge(board, piece, piece_offset)
            completed_lines = [i for i, row in enumerate(board) if ' ' not in row]
            for line in completed_lines:
                clear_line(board, line)

            piece = get_random_piece()
            piece_offset = [0, BOARD_WIDTH // 2 - len(piece[0]) // 2]

            if collide(board, piece, piece_offset):
                break

        draw_board(stdscr, board)

        key = stdscr.getch()

        if key == curses.KEY_LEFT and piece_offset[1] > 0 and not collide(board, piece, [piece_offset[0], piece_offset[1] - 1]):
            piece_offset[1] -= 1
        elif key == curses.KEY_RIGHT and piece_offset[1] + len(piece[0]) < BOARD_WIDTH and not collide(board, piece, [piece_offset[0], piece_offset[1] + 1]):
            piece_offset[1] += 1
        elif key == curses.KEY_DOWN and piece_offset[0] + len(piece) < BOARD_HEIGHT and not collide(board, piece, [piece_offset[0] + 1, piece_offset[1]]):
            piece_offset[0] += 1
        elif key == curses.KEY_UP:
            rotated_piece = rotate(piece)
            if piece_offset[1] + len(rotated_piece[0]) <= BOARD_WIDTH and not collide(board, rotated_piece, piece_offset):
                piece = rotated_piece

if __name__ == "__main__":
    curses.wrapper(main)
