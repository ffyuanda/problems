from utilities import *
import copy
DEV_MODE = False
game_over = True
quit = False

test_board = [[1, 0, 0, 0],
              [4, 0, 0, 2],
              [16, 0, 0, 0],
              [1024, 0, 0, 0]]
board = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]


def basic_move(in_row):
    """Moving a cell left (pressing A).
    :return: None"""

    for col in range(4):
        for i in range(col-1, -1, -1):
            # read from the next left cell to check left availability
            if in_row[i] == 0:
                # read the next zero on the left
                latest_zero = i
                if i == 0:
                    # read all the way to the left end
                    in_row[i] = in_row[col]
                    in_row[col] = 0
                continue
            else:
                # meet a non-zero number (get blocked) then move it
                if i == col-1:
                    # get blocked immediately
                    break
                in_row[latest_zero] = in_row[col]
                in_row[col] = 0
                break


def left_collapse(in_row):
    """Collapse the moved row (add the same number up).
    :return: None"""

    for i in range(len(in_row)-1):
        curr = in_row[i]
        next = in_row[i+1]

        if curr == next:
            in_row[i] = curr * 2
            in_row[i+1] = 0

        else:
            continue


def move_row(in_row):
    """Moving a row to left.
    :param in_row: the row that need to be moved
    :return None"""
    basic_move(in_row)
    left_collapse(in_row)
    basic_move(in_row)


def move_board(in_board):
    """Moving a board to the left (pressing A/a).
    :param in_board: the board
    :return None"""

    for row in in_board:
        move_row(row)


def rotation(in_board):
    """Rotate the board 90 degrees clockwise.
    :return A board after rotation
    """
    after_board = [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
    for col in range(len(in_board[0]) - 1, -1, -1):
        for row in range(len(in_board)):
            after_board[row][col] = in_board[3-col][row]

    return after_board


def place_random_wrapper(in_board):
    """Wrapping the place_random function up for convenience.
    :param in_board: the board
    :return None"""
    next_random = place_random(in_board)
    in_board[next_random['row']][next_random['column']] = next_random['value']


def move(in_board):
    """Respond to user's input and move the board.
    :param in_board: the board
    :return the board after move"""
    checker = copy.deepcopy(in_board)
    after_board = copy.deepcopy(in_board)
    direc = str.upper(input())
    global quit

    if direc == "W":
        # Moving up
        for i in range(3):
            after_board = rotation(after_board)
        move_board(after_board)
        after_board = rotation(after_board)

    elif direc == "S":
        # Moving down
        after_board = rotation(after_board)
        move_board(after_board)
        for i in range(3):
            after_board = rotation(after_board)
    elif direc == "A":
        # Moving left
        move_board(after_board)
    elif direc == "D":
        # Moving right
        for i in range(2):
            after_board = rotation(after_board)
        move_board(after_board)
        for i in range(2):
            after_board = rotation(after_board)
    elif direc == 'Q':
        print('Goodbye')
        # Change the quit to true to end the game.
        quit = True
    else:
        # For the invalid inputs, keep the board the same.
        pass

    # See if the board has been changed. Only the board after a change
    # can be added a random number.
    if checker != after_board:
        # Place a random int on the board.
        place_random_wrapper(after_board)

    return after_board


def empty_check(in_board):
    """
    Check if the current board has any empty cells (has any 0s).
    :param in_board: the board
    :return: if the board has any empty cells (True) or not (False)
    """
    empty = False
    for row in range(len(in_board)):
        for col in range(len(in_board[0])):
            if in_board[row][col] == 2048:
                return 'win'
            elif in_board[row][col] == 0:
                empty = True

    return empty


def game_over(in_board):
    """
    Check if the game is over (the player is lost) by rotating the board around
    and try to move the board until it cannot be moved from any direction, then
    we can confirm that the game is over. Vice versa.
    :param in_board: the board
    :return: a boolean show win (False) or lost (True)
    """
    checker = copy.deepcopy(in_board)
    game_over = True
    for i in range(4):
        checker = rotation(checker)
        comparison = copy.deepcopy(checker)
        move_board(comparison)

        if comparison != checker:
            game_over = False
    return game_over


def main(game_board):
    """
    project_2048 main function, runs a game of project_2048 in the console.

    Uses the following keys:
    w - shift up
    a - shift left
    s - shift down
    d - shift right
    q - ends the game and returns control of the console
    :param game_board: a 4x4 2D list of integers representing a game of project_2048
    :return: returns the ending game board
    """
    # Initial game board display.
    global quit
    if empty_check(game_board):
        place_random_wrapper(game_board)
        place_random_wrapper(game_board)
    print_board(game_board)

    while True:

        if not empty_check(game_board) and game_over(game_board):
            print('Game Over')
            return game_board

        game_board = move(game_board)

        # When q(uit) is entered
        if quit:
            quit = False
            return game_board

        # when not quit
        else:
            print_board(game_board)
            if empty_check(game_board) == 'win':
                print('You Win')
                return game_board


if __name__ == "__main__":

    main(board)
