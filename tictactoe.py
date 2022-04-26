"""
Tic Tac Toe Player
"""
import random
import copy
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
    
    # check which player has the turn
    x_counter = 0
    o_counter = 0
    for row in board:
        for col in row:
            if col == X:
                x_counter += 1
            elif col == O:
                o_counter += 1

    return O if o_counter < x_counter else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Returns the cooradinates of the empty slots
    Returns empty set if now slot is empty
    """
    empty_slots = set()
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                empty_slots.add((row, col))

    return empty_slots


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    return a new data structure that represents the new state after playing
    move(i, j) without modifying the original one
    cuz that helps the minimax to consider many states
    """
    #copy the input board into the new data structure
    new_board = copy.deepcopy(board)

    # apply the new action to the new board
    row = action[0]
    col = action[1]
    new_board[row][col] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    a player win when he makes a three moves vertically, horizontally, or diagonally
    """

    winner_vert = checkVertically(board)
    if winner_vert:
        return winner_vert

    winner_hori = checkHorizontally(board)
    if winner_hori:
        return winner_hori

    winner_diagonal = checkDiagonally(board)
    if winner_diagonal:
        return winner_diagonal
    
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return True if winner(board) or (not isThereEmptySlot(board)) else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):

        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    The move returned should be the optimal action (i, j) 
    that is one of the allowable actions on the board. If multiple moves are equally optimal,
    any of those moves is acceptable.
    If the board is a terminal board, the minimax function should return None.
    """
    if terminal(board):
        return None

    Max = -math.inf
    Min = math.inf

    if player(board) == X:
        return maxValue(board, Max, Min)[1]
    else:
        return minValue(board, Max, Min)[1]


################### Helpers ##################################


def maxValue(board, Max, Min):
    '''
    this tries to maximize the utitliy value
    '''
    if terminal(board):
        return (utility(board), None)
    
    move = None
    val = -math.inf
    for action in actions(board):
        consider_oppenent = minValue(result(board, action), Max, Min)[0]
        Max = max(Max, consider_oppenent)

        if consider_oppenent > val:
            val = consider_oppenent
            move = action

        if Max >= Min:
            break

    return (val, move)


def minValue(board, Max, Min):
    '''
    Minimizing the utility value of board
    '''
    
    if terminal(board):
        return (utility(board), None)
    
    move = None
    val = math.inf
    for action in actions(board):
        consider_oppenent = maxValue(result(board, action), Max, Min)[0]
        Min = min(Min, consider_oppenent)

        if consider_oppenent < val:
            val = consider_oppenent
            move = action

        if Max >= Min:
            break

    return (val, move)


def getMaxPlayer(board):
    '''
    the max player is the one who starts the game
    '''
    x_count = 0
    o_count = 0
    for row in board:
        for col in row:
            if col == X:
                x_count += 1
            elif col == O:
                o_count += 1
    
    # max has the more count
    return X if x_count > o_count else O


def checkVertically(board):
    # check vertically
    for row in board:
        if row[0] == row[1] == row[2] and row[1] != EMPTY:
            winner = row[0]
            return winner

    return None

def checkHorizontally(board):
    # check horizonally
    row1 = iter(board[0])
    row2 = iter(board[1])
    row3 = iter(board[2])

    while True:
        try:
            col1 = next(row1)
            col2 = next(row2)
            col3 = next(row3)
            if col1 == col2 == col3 and col1 != EMPTY:
                winner = col1
                return winner

        except StopIteration:
            return None


def checkDiagonally(board):
    
    main_diagonal = []
    secondary_diagonal = []
    for i in range(len(board)):
        for j in range(len(board)):
            # main diagonal condition
            if i == j:
                main_diagonal.append(board[i][j])

            # secondary diagonal conition
            if (i + j) == (len(board) - 1):
                secondary_diagonal.append(board[i][j])

    if main_diagonal[0] == main_diagonal[1] == main_diagonal[2] and main_diagonal[1] != EMPTY:
        return main_diagonal[0]

    if secondary_diagonal[0] == secondary_diagonal[1] == secondary_diagonal[2] and secondary_diagonal[1] != EMPTY:
        return secondary_diagonal[0]
    
    return None


def isThereEmptySlot(board):
    '''
    True: there is still empty slots
    False: no emtpy slots
    '''
    empty_slot = False
    for row in board:
        for col in row:
            if col == EMPTY:
                empty_slot = True
    return empty_slot
            
