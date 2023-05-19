import numpy as np
import random as rand
import reversi
import chip_node


class ReversiBot:
    def __init__(self, move_num):
        self.move_num = move_num

    def make_move(self, state):
        self.create_root(state)
        move = self.new_minimax_root(state)
        print("I suggest moving here:", move)
        return move

    def create_root(self, state):
        points = self.heuristic_eval(state)
        self.root_node = chip_node.Node(
            points, state.turn, state.board.copy())
        depth = 0
        valid_moves = state.get_valid_moves()
        for x in range(0, len(valid_moves)):
            self.create_tree(state, valid_moves[x], self.root_node, depth)

    def create_tree(self, state, move, node, depth):
        DEPTH_TO_SEARCH = 3
        if depth > DEPTH_TO_SEARCH:
            return None
        node_state = self.get_next_state(state, move)
        valid_moves = node_state.get_valid_moves()
        points = self.heuristic_eval(node_state)
        child_node = chip_node.Node(
            points, node_state.turn, node_state.board.copy(), move)
        node.insert_child(child_node)

        for x in range(0, len(valid_moves)):
            self.create_tree(node_state, valid_moves[x], child_node, depth + 1)

    # First minimax run keeps track of the best move

    def new_minimax_root(self, state):
        valid_moves = state.get_valid_moves()
        best_points = 0
        best_move = valid_moves[0]
        for n in range(0, len(self.root_node.children)):
            points = self.new_minimax(self.root_node.children[n], True, float('inf'), float('-inf'))
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
                points = max(points, self.new_minimax(node.children[n], False, alpha, beta))
                alpha = max(points, alpha)
                if beta <= alpha:
                    break
                
        else:
            # impliment the beta pruning here
            points = 1000
            for n in range(0, len(node.children)):
                points = min(points, self.new_minimax(node.children[n], True, alpha, beta))
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
                if (state.board[x][y] == state.turn):
                    points += values[x][y]
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
            return 1000
        else:
            # We Lose
            return -1000

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
