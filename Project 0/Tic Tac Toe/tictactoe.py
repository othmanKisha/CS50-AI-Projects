"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # If the game ends, we don't care about the player
    if terminal(board):
        return None

    # Looping over the board to count X and O, if both 0 then the player is X
    xcount = sum([1 for i in range(3) for j in range(3) if board[i][j] == X])
    ocount = sum([1 for i in range(3) for j in range(3) if board[i][j] == O])

    # even if both are 0, then x will play
    return X if ocount == xcount else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Check if the game is finished
    if terminal(board):
        return None

    # The set of all possible actions
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if action is not valid
    if (action[0] < 0 or action[0] > 2) or (action[1] < 0 or action[1] > 2):
        raise Exception(" Out of bound exception.")

    # The player with the current turn
    turn = player(board)

    # copy the board
    result = initial_state()
    for row in range(3):
        for col in range(3):
            result[row][col] = board[row][col]

    # Making the action
    result[action[0]][action[1]] = turn

    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Listing the columns
    cols = [[board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]]]

    # Check for diagonals
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]

    if board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    # Loop for checking columns
    for col in cols:
        # Check if all elements in column are equal
        if all(cell == col[0] and col[0] != EMPTY for cell in col):
            return col[0]

    # Loop for checking rows
    for row in board:
        # Check if all elements in a row are equal
        if all(cell == row[0] and row[0] != EMPTY for cell in row):
            return row[0]

    # if there still no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    # Check if every cell is filled
    return True if winner(board) != None or all(cell for row in board for cell in row) else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Assuming the we have a terminal board
    return 1 if winner(board) == X else -1 if winner(board) == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Method to retreive the max/min-value
    def value(board, maxmin):

        # Check if the game is terminated, then return utility
        if terminal(board):
            return utility(board)

        # Set of all possible actions
        actions_set = actions(board)

        # Return the min/max-value of all the max/min-values in the list of resulting utilities from actions
        return min([
            value(result(board, action), "max") for action in actions_set
        ]) if maxmin == "min" else max([
            value(result(board, action), "min") for action in actions_set
        ])

    # Checking for the turn
    turn = player(board)

    # List of all possible actions
    actions_set = actions(board)

    # Looping over all possible actions
    for action in actions_set:
        new_board = result(board, action)

        # If turn is X ==> we look for max-value
        if turn == X:
            # If the min-value resulting from the board after making this action
            # is the same as max-value of the current board ==> return the action
            if value(new_board, "min") == value(board, "max"):
                return action

        # If turn is O ==> we look for min-value
        elif turn == O:
            # If the max-value resulting from the board after making this action
            # is the same as min-value of the current board ==> return the action
            if value(new_board, "max") == value(board, "min"):
                return action
