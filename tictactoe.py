 
#the player function takes a board state as input and returns which player's turn it is 
#player X has the first move 
import math 
import copy 
import pygame 
X = "X"
O = "O"
EMPTY = None 

def initial_state():
    #returns the initial state of the board
    #3 by 3 grid 
    return [[EMPTY, EMPTY, EMPTY], 
            [EMPTY, EMPTY, EMPTY], 
            [EMPTY, EMPTY, EMPTY]] 

def player(board):
    #returns which player has the next turn 
    countX = 0
    countO = 0 

    #use a nested loop to loop through all the rows and columns
    for row in range(len(board)):
        for col in range(len(board[row])): 
            if board[row][col] == X:
                countX += 1
            if board[row][col] == O:
                countO += 1
    
    if countX > countO:
        return O
    else: 
        return X

def actions(board):
    #returns a set of all possible actions (i, j) available on the board
    all_possible_moves = set()
    for row in range(len(board)): 
        for col in range(len(board[0])): 
            if board[row][col] == EMPTY:
                all_possible_moves.add((row, col))
    
    return all_possible_moves 
    #the set all_possible_moves is a tuple (i, j) 

def result(board, action):
    #returns the new board after making the move (i, j) 
    if action not in actions(board):
        raise Exception("Invalid Move") 
    
    row, col = action #row = i and col = j 
    board_copy = copy.deepcopy(board) #making a copy of the current game board 
    board_copy[row][col] = player(board) #checking which player made the move 
    return board_copy 

def check_row(board, player): 
    for row in range(len(board)): 
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True 
    return False 

def check_col(board, player): 
    for col in range(len(board)): #len(board) = 3 
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True 
    return False 

#check both diagonals 
def check_diag1(board, player):
    count = 0 
    for row in range(len(board)): 
        for col in range(len(board[row])): 
            if row == col and board[row][col] == player: 
                count += 1 
    if count == 3: 
        return True 
    else: 
        return False 

def check_diag2(board, player):
    count = 0 
    for row in range(len(board)): 
        for col in range(len(board[row])): 
            if (len(board) - row - 1) == col and board[row][col] == player: 
                count += 1 
    if count == 3: 
        return True 
    else: 
        return False 

def winner(board): 
    #returns the winner of the game if the game doesn't end in a tie 
    if check_row(board, X) or check_col(board, X) or check_diag1(board, X) or check_diag2(board, X): 
        return X 
    elif check_row(board, O) or check_col(board, O) or check_diag1(board, O) or check_diag2(board, O): 
        return O 
    else: 
        return None #no winner, game ends in a tie 

def terminal(board): 
    #returns true if the game is over and false otherwise 
    if winner(board) == X: 
        return True 
    if winner(board) == O: 
        return True 
    for row in range(len(board)): 
        for col in range(len(board[row])): 
            if board[row][col] == EMPTY: 
                return False 
    return True 

def utility(board): 
    #return 1 if X wins, -1 if O wins and 0 if the game ends in a tie 
    if winner(board) == X: 
        return 1 
    elif winner(board) == O: 
        return -1 
    else: 
        return 0 
    
def max_value(board): 
    v = -math.inf #negative infinity 
    if terminal(board): 
        return utility(board) 
    for action in actions(board): 
        v = max(v, min_value(result(board, action))) 
    return v 

def min_value(board): 
    v = math.inf #infinity 
    if terminal(board): 
        return utility(board) 
    for action in actions(board): 
        v = min(v, max_value(result(board, action))) 
    return v 

#add more comments 
def minimax(board): 
    #returns the optimal move for the current player 
    #we want to maximize the moves of player X 
    if terminal(board): 
        return None 
    elif player(board) == X: 
        plays = [] #an empty list 
        for action in actions(board): 
            plays.append([min_value(result(board, action)), action]) 
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1] 
    

    #case for player O 
    if terminal(board): 
        return None 
    elif player(board) == O: 
        plays = [] #an empty list 
        #looping over all possible moves 
        for action in actions(board): 
            plays.append([max_value(result(board, action)), action]) 
        return sorted(plays, key=lambda x: x[0])[0][1] 
