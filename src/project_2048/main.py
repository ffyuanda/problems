import utilities
DEV_MODE = False


def main(game_board: [[int, ], ]) -> [[int, ], ]:
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
    # Initialize board's first cell

    # You are not required to implement develop mode, but it is encouraged to do so.
    # Develop mode allows you to input the location of the next piece that will be
    # placed on the board, rather than attempting to debug your code with random
    # input values.
    if DEV_MODE:
        # This line of code handles the input of the develop mode.
        column, row, value = (int(i) for i in input("column,row,value:").split(','))

        # OPTIONAL: place the piece in the corresponding cell on the game board
    else:
        # TODO: generate a random piece and location using the place_random function
        # TODO: place the piece at the specified location
        pass

    # Initialize game state trackers

    # Game Loop
    while True:
        break
        # TODO: Reset user input variable

        # TODO: Take computer's turn
        # place a random piece on the board
        # check to see if the game is over using the game_over function

        # TODO: Show updated board using the print_board function

        # TODO: Take user's turn
        # Take input until the user's move is a valid key
        # if the user quits the game, print Goodbye and stop the Game Loop
        # Execute the user's move

        # Check if the user wins
    return game_board


def game_over(game_board: [[int, ], ]) -> bool:
    """
    Query the provided board's game state.

    :param game_board: a 4x4 2D list of integers representing a game of project_2048
    :return: Boolean indicating if the game is over (True) or not (False)
    """
    # TODO: Loop over the board and determine if the game is over
    return False  # TODO: Don't always return false


if __name__ == "__main__":
    main([[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]])
