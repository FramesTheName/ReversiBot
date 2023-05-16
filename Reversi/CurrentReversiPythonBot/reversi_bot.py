import numpy as np
import random as rand
import reversi

class ReversiBot:
    def __init__(self, move_num):
        self.move_num = move_num

    def make_move(self, state):
        '''
        This is the only function that needs to be implemented for the lab!
        The bot should take a game state and return a move.

        The parameter "state" is of type ReversiGameState and has two useful
        member variables. The first is "board", which is an 8x8 numpy array
        of 0s, 1s, and 2s. If a spot has a 0 that means it is unoccupied. If
        there is a 1 that means the spot has one of player 1's stones. If
        there is a 2 on the spot that means that spot has one of player 2's
        stones. The other useful member variable is "turn", which is 1 if it's
        player 1's turn and 2 if it's player 2's turn.

        ReversiGameState objects have a nice method called get_valid_moves.
        When you invoke it on a ReversiGameState object a list of valid
        moves for that state is returned in the form of a list of tuples.

        Move should be a tuple (row, col) of the move you want the bot to make.
        '''
        valid_moves = state.get_valid_moves()
        print("I move here:")
        print(self.minimax_root(state))
        move = rand.choice(valid_moves) # Moves randomly...for now
        return move
    
    # First minimax run keeps track of the best move
    def minimax_root(self, state):
        valid_moves = state.get_valid_moves()
        alpha = 0
        beta = 0
        best_value = -1000000
        best_move = valid_moves[0]
        for move in valid_moves:
            value = self.minimax(self.get_next_state(state, move), 1, False, alpha, beta)
            best_value = max(best_value, value)
            if value == best_value:
                best_move = move
            alpha = max(best_value, alpha)
            if beta <= alpha:
                break
        return best_move
    
    # The recursive minimax function that propagates forward the best value
    def minimax(self, state, depth, isMaximizingPlayer, alpha, beta):
        DEPTH_TO_SEARCH = 4
        valid_moves = state.get_valid_moves()

        # Leaf Node
        if len(valid_moves) == 0: 
            return self.get_winner(state.board)
        
        # Reached search limit
        if depth > DEPTH_TO_SEARCH: 
            return self.heuristic_eval(state)
        
        # Maximizer
        if isMaximizingPlayer :
            best_value = float('-inf')
            for move in valid_moves:
                value = self.minimax(self.get_next_state(state, move), depth+1, False, alpha, beta)
                best_value = max( best_value, value)
                alpha = max(best_value, alpha)
                if beta <= alpha:
                    break
            return best_value
        # Minimizer
        else :
            best_value = float('inf')
            for move in valid_moves :
                value = self.minimax(self.get_next_state(state, move), depth+1, True, alpha, beta)
                best_value = min( best_value, value) 
                beta = min( beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    # Heuristic function to look at the board and evaluate its current value    
    def heuristic_eval(self, state):
        return 101

    # A simple function to see who has won the game at the current leaf node
    def get_winner(self, board):
        myPoints = 0
        for row in board:
            for number in row:
                if number == self.move_num:
                    myPoints += 1

        if(myPoints > 32):
            # We Win
            return myPoints * 99999
        else:
            # We Lose
            return myPoints * -99999
        
    # A simple function to give the board a move and update the pieces to look at the future   
    def get_next_state(self, state, move):
        new_board = state.board
        new_board[move[0],move[1]] = state.turn

        # Flip left right pieces
        if state.turn in new_board[move[0]]:

            # Flip Right of Move
            if move[1] != 7:
                flipped = []
                for x in range(move[1] + 1, 8):
                    if new_board[move[0]][x] == 0:
                        break
                    if x == state.turn:
                        for y in flipped:
                            new_board[move[0]][y] = state.turn
                        break
                    flipped.append(x)

            # Flip Left of Move
            if move[1] != 0:
                flipped = []
                for x in range(move[1] - 1, -1, -1):
                    if new_board[move[0]][x] == 0:
                        break
                    if new_board[move[0]][x] == state.turn:
                        for y in flipped:
                            new_board[move[0]][y] = state.turn
                        break
                    flipped.append(x)
        
        # Flip Up of Move
        if move[0] != 7:
            flipped = []
            for x in range(move[0] + 1, 8):
                if new_board[x][move[1]] == 0:
                    break
                if new_board[x][move[1]] == state.turn:
                    for y in flipped:
                        new_board[y][move[1]] = state.turn
                    break
                flipped.append(x)

        # Flip Down of Move
        if move[0] != 0:
            flipped = []
            for x in range(move[0] - 1, -1, -1):
                if new_board[x][move[1]] == 0:
                    break
                if new_board[x][move[1]] == state.turn:
                    for y in flipped:
                        new_board[y][move[1]] = state.turn
                    break
                flipped.append(x)
        
        # Flip Up-Right of Move
        if move[0] != 7 and move[1] != 7:
            flipped = []
            for x in range(1, 8):
                if move[0] + x == 8 or move[1] + x == 8:
                    break
                if new_board[move[0] + x][move[1] + x] == 0:
                    break
                if new_board[move[0] + x][move[1] + x] == state.turn:
                    for y in flipped:
                        new_board[move[0] + y][move[1] + y] = state.turn
                    break
                flipped.append(x)

        # Flip Down-Left of Move
        if move[0] != 0 and move[1] != 0:
            flipped = []
            for x in range(1, 8):
                if move[0] - x == -1 or move[1] - x == -1:
                    break
                if new_board[move[0] - x][move[1] - x] == 0:
                    break
                if new_board[move[0] - x][move[1] - x] == state.turn:
                    for y in flipped:
                        new_board[move[0] - y][move[1] - y] = state.turn
                    break
                flipped.append(x)
        
        # Flip Down-Right of Move
        if move[0] != 7 and move[1] != 0:
            flipped = []
            for x in range(1, 8):
                if move[0] + x == 8 or move[1] - x == -1:
                    break
                if new_board[move[0] + x][move[1] - x] == 0:
                    break
                if new_board[move[0] + x][move[1] - x] == state.turn:
                    for y in flipped:
                        new_board[move[0] + y][move[1] - y] = state.turn
                    break
                flipped.append(x)

        # Flip Down-Right of Move
        if move[0] != 0 and move[1] != 7:
            flipped = []
            for x in range(1, 8):
                if move[0] - x == -1 or move[1] + x == 8:
                    break
                if new_board[move[0] - x][move[1] + x] == 0:
                    break
                if new_board[move[0] - x][move[1] + x] == state.turn:
                    for y in flipped:
                        new_board[move[0] - y][move[1] + y] = state.turn
                    break
                flipped.append(x)

        if state.turn == 2:
            new_turn = 1
        else:
            new_turn = 2
        
        # create next_state and return it
        next_state = reversi.ReversiGameState(new_board, new_turn)
        return next_state

