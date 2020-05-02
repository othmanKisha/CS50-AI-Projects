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

    # Counting the number of x
    xcount = 0
    # counting the number of o
    ocount = 0

    # Looping over the board to count X and O, if both 0 then the player is X
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                xcount += 1
            elif board[i][j] == O:
                ocount += 1

    # even if both are 0, then x will play
    if ocount == xcount:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Check if the game is finished
    if terminal(board):
        return None

    # The set of all possible actions
    actions_set = set()

    # Looping over the board
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_set.add((i, j))

    return actions_set


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
    if winner(board) != None:
        return True

    # Check if every cell is filled
    is_full = all(cell for row in board for cell in row)
    if is_full:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Assuming the we have a terminal board
    if winner(board) == X:
        # In case X wins
        return 1
    elif winner(board) == O:
        # In case O wins
        return -1
    else:
        # In case no body wins
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Checking for the turn
    turn = player(board)
    # List of all possible actions
    actions_set = actions(board)

    # Looping over all possible actions
    for action in actions_set:
        new_board = result(board, action)

        # If turn is X ==> we look for max-value
        if turn == X:
            """ 
            If the min-value resulting from the board after making this action
            is the same as max-value of the current board ==> return the action
            """
            if min_value(new_board) == max_value(board):
                return action

        # If turn is O ==> we look for min-value
        elif turn == O:
            """ 
            If the max-value resulting from the board after making this action
            is the same as min-value of the current board ==> return the action
            """
            if max_value(new_board) == min_value(board):
                return action


def max_value(board):

    # Check if the game is terminated, then return utility
    if terminal(board):
        return utility(board)

    # Set of all possible actions
    actions_set = actions(board)
    # List of resulting utilities from actions
    utilities = []

    # Looping over the actions and appending the min-value result
    for action in actions_set:
        new_board = result(board, action)
        utilities.append(min_value(new_board))

    # Return the max-value of all the min-values in utilities list
    return max(utilities)


def min_value(board):

    # Check if the game is terminated, then return utility
    if terminal(board):
        return utility(board)

    # Set of all possible actions
    actions_set = actions(board)
    # List of resulting utilities from actions
    utilities = []

    # Looping over the actions and appending the max-value result
    for action in actions_set:
        new_board = result(board, action)
        utilities.append(max_value(new_board))

    # Return the min-value of all the max-values in utilities list
    return min(utilities)
