import numpy as np
import random as rand
import reversi

class ReversiBot:
    def __init__(self, move_num):
        self.move_num = move_num

    def make_move(self, state):
        print("I suggest moving here:")
        move = self.minimax_root(state)
        print(move)
        return move
    
    # First minimax run keeps track of the best move
    def minimax_root(self, state):
        valid_moves = state.get_valid_moves()
        alpha = float('-inf')
        beta = float('inf')
        best_value = float('-inf')
        best_move = valid_moves[0]
        for move in valid_moves:
            value = self.minimax(self.get_next_state(state, move), 1, False, alpha, beta)
            best_value = max(best_value, value)
            alpha = max(value, alpha)
            if value == best_value:
                best_move = move
        return best_move
    
    # The recursive minimax function that propagates forward the best value
    def minimax(self, state, depth, isMaximizingPlayer, alpha, beta):
        DEPTH_TO_SEARCH = 20
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
                alpha = max(value, alpha)
                if beta <= alpha:
                    break
            return best_value
        # Minimizer
        else :
            worst_value = float('inf')
            for move in valid_moves :
                value = self.minimax(self.get_next_state(state, move), depth+1, True, alpha, beta)
                worst_value = min( worst_value, value)
                beta = min( beta, value) 
                if beta <= alpha:
                    break
            return worst_value

    # Heuristic function to look at the board and evaluate its current value    
    def heuristic_eval(self, state):
        print("heuristic eval")
        points = 0
        values = [
            [120, -20,  20,   5,   5,  20, -20, 120],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [20,  -5,  15,   3,   3,  15,  -5,  20],
            [5,  -5,   3,   3,   3,   3,  -5,   5],
            [5,  -5,   3,   3,   3,   3,  -5,   5],
            [20,  -5,  15,   3,   3,  15,  -5,  20],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [120, -20,  20,   5,   5,  20, -20, 120]
        ]
        for x in range(0, 7):
            for y in range(0, 7):
                if (state.board[x][y] == self.move_num):
                    points += values[x][y]
        return points

    # A simple function to see who has won the game at the current leaf node
    def get_winner(self, board):
        myPoints = 0
        for row in board:
            for number in row:
                if number == self.move_num:
                    myPoints += 1

        if(myPoints > 32):
            # We Win
            return myPoints * 10
        else:
            # We Lose
            return myPoints * -10
        
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

        # Flip Up-Right of Move
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

