import numpy as np
import random as rand
import reversi
import chip_node


class ReversiBot:
    global DEPTH_TO_SEARCH
    DEPTH_TO_SEARCH = 3

    def __init__(self, move_num):
        self.move_num = move_num

    def make_move(self, state):
        valid_moves = state.get_valid_moves()
        if len(valid_moves) >= 7:
            DEPTH_TO_SEARCH = 1
        elif len(valid_moves) >= 4:
            DEPTH_TO_SEARCH = 2
        elif len(valid_moves) >= 2:
            DEPTH_TO_SEARCH = 3
        else:
            DEPTH_TO_SEARCH = 4

        #Builds out our tree
        self.create_root(state)

        #Calculates best move
        move = self.new_minimax_root(state)
        print(state.board)
        print("I suggest moving here:", move)

        #Changes root node
        for x in range(0, len(self.root_node.children)):
            if (move == self.root_node.children[x].move):
                self.root_node = self.root_node.children[x]
                break
        
        #Send move
        return move

    #Starts building our searchable tree
    def create_root(self, state):

        #If a root node already existed (i.e. a best move?)
        if hasattr(self, "root_node"):
            move = self.assign_root(self.root_node.board, state.board)

            for x in range(0, len(self.root_node.children)):
                if (move == self.root_node.children[x].move):
                    self.root_node = self.root_node.children[x]
                    break
            
            #Create tree at current root node plus the depth neccessary
            self.traverse_tree(self.root_node, self.root_node.get_depth())

        #If a root node does not exist create a new node
        else:
            points = self.heuristic_eval(state)
            self.root_node = chip_node.Node(
                points, state.turn, state.board.copy())
            depth = 0
            valid_moves = state.get_valid_moves()
            for x in range(0, len(valid_moves)):
                self.create_tree(state, valid_moves[x], self.root_node, depth)

    def assign_root(self, previous_board, current_board):
        for x in range(0, 8):
            for y in range(0, 8):
                if (previous_board[x][y] == 0 and current_board[x][y] != 0):
                    return (x, y)

    def traverse_tree(self, node, depth):

        #If I have made it to the required depth to search
        if depth > DEPTH_TO_SEARCH:
            return None
        
        #If I have no children in the tree
        if (len(node.children) == 0):
            game_state = reversi.ReversiGameState(node.board.copy(), node.turn)
            valid_moves = game_state.get_valid_moves()

            #Make sure I have valid moves (Not a leaf node)
            if (len(valid_moves) == 0):
                return
        
            #Continue tree propigation
            for x in range(0, len(valid_moves)):
                self.create_tree(game_state, valid_moves[x], node, depth - 1)
        
        #Keep searching children nodes        
        else:
            for x in range(0, len(node.children)):
                self.traverse_tree(node.children[x], depth)

    
    def create_tree(self, state, move, node, depth):
        #Make sure I do not go too deep
        if depth > DEPTH_TO_SEARCH:
            return None
        
        node_state = self.get_next_state(state, move)
        valid_moves = node_state.get_valid_moves()

        #Check for child nodes
        if (len(valid_moves) != 0):
            points = self.heuristic_eval(node_state)
        else:
            points = self.get_winner(node_state.board)
        
        #Make me a child node
        child_node = chip_node.Node(points, node_state.turn, node_state.board.copy(), move)
        node.insert_child(child_node)

        #Propigate my children ndoes
        for x in range(0, len(valid_moves)):
            self.create_tree(node_state, valid_moves[x], child_node, depth + 1)

    # A function that returns true if the board is in a leaf node
    def is_leaf_node(self, state):
        for row in state.board:
            if 0 in row:
                return False
        return True

    # First minimax run keeps track of the best move

    def new_minimax_root(self, state):
        valid_moves = state.get_valid_moves()
        best_points = 0
        best_move = valid_moves[0]
        for n in range(0, len(self.root_node.children)):
            points = self.new_minimax(
                self.root_node.children[n], True, float('inf'), float('-inf'))
            if (points > best_points):
                best_points = points
                best_move = self.root_node.children[n].move

        return best_move

    def new_minimax(self, node, isMaximizingPlayer, alpha, beta):

        # if there are no more valid moves, then return if the person is the winner.
        if len(node.children) == 0:
            return node.points
        points = 0
        if isMaximizingPlayer:
            # impliment the beta pruning here
            points = -1000
            for n in range(0, len(node.children)):
                points = max(points, self.new_minimax(
                    node.children[n], False, alpha, beta))
                alpha = max(points, alpha)
                if beta <= alpha:
                    break

        else:
            # impliment the beta pruning here
            points = 1000
            for n in range(0, len(node.children)):
                points = min(points, self.new_minimax(
                    node.children[n], True, alpha, beta))
                beta = min(beta, points)
                if beta <= alpha:
                    break
        return points

    # Heuristic function to look at the board and evaluate its current value
    # this function will give 1 point for every chip the player has. Furthermore,
    # it will give an extra 5 points for every edge piece the player has and 10 points for a corner piece.
    def heuristic_eval(self, state):
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
                elif state.board[x][y] == 0:
                    points += 0
                else:
                    points -= values[x][y]
        return points

    # A simple function to see who has won the game at the current leaf node
    def get_winner(self, board):
        myPoints = 0
        for row in board:
            for number in row:
                if number == self.move_num:
                    myPoints += 1

        if (myPoints > 32):
            # We Win
            return 100000
        else:
            # We Lose
            return -100000

    # A function that changes whose turn it is
    def change_turn(self, state):
        if state.turn == 2:
            new_turn = 1
        else:
            new_turn = 2
        return reversi.ReversiGameState(state.board.copy(), new_turn)

    # A simple function to give the board a move and update the pieces to look at the future
    def get_next_state(self, state, move):
        new_board = state.board.copy()
        new_board[move[0], move[1]] = state.turn

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
