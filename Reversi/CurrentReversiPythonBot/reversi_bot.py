import numpy as np
import random as rand
import reversi
import chip_node


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
        self.create_root(state)
        move = self.new_minimax_root(state)
        print("I suggest moving here:", move)
        # move = rand.choice(valid_moves)  # Moves randomly...for now
        return move

    def create_root(self, state):
        points = self.heuristic_eval(state)
        # instead of recalculating everything everytime, if there is a root node, then
        # this function will go through and assign the root_node to the current state.
        if hasattr(self, "root_node"):
            self.assign_root(self.root_node, np.array(state.board), 0)
            self.traverse_tree(self.root_node)
        else:
            self.root_node = chip_node.Node(
                points, state.turn, state.board.copy())
            depth = 0
            valid_moves = state.get_valid_moves()
            for x in range(0, len(valid_moves)):
                self.create_tree(state, valid_moves[x], self.root_node, depth)

    def assign_root(self, node, board, depth):
        if (depth > 2):
            return False

        n_one = np.array(node.board)
        if ((n_one == board).all()):
            self.root_node = node
            return True
        else:
            for x in range(0, len(node.children)):
                if (self.assign_root(node.children[x], board, depth + 1)):
                    return True

    def traverse_tree(self, node):
        if (len(node.children) == 0):
            game_state = reversi.ReversiGameState(node.board.copy(), node.turn)
            valid_moves = game_state.get_valid_moves()
            if (len(valid_moves) == 0):
                return
            for x in range(0, len(valid_moves)):
                self.create_tree(game_state, valid_moves[x], node, 2)
        else:
            for x in range(0, len(node.children)):
                self.traverse_tree(node.children[x])

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
        print('validMoves: ', valid_moves)

        best_points = 0
        best_move = valid_moves[0]
        for n in range(0, len(self.root_node.children)):
            points = self.new_minimax(self.root_node.children[n], True)
            if (points > best_points):
                best_points = points
                best_move = self.root_node.children[n].move

        return best_move

    def new_minimax(self, node, isMaximizingPlayer):
        print('new_minimax')

        # if there are no more valid moves, then return if the person is the winner.
        if len(node.children) == 0:
            return node.points
        points = 0
        if isMaximizingPlayer:
            # impliment the beta pruning here
            points = -1000
            for n in range(0, len(node.children)):
                points = max(points, self.new_minimax(node.children[n], False))
                print(points)
        else:
            # impliment the beta pruning here
            points = 1000
            for n in range(0, len(node.children)):
                points = min(points, self.new_minimax(node.children[n], True))
                print(points)
        return points

    def minimax_root(self, state):
        valid_moves = state.get_valid_moves()
        print('validMoves: ', valid_moves)
        alpha = 0
        beta = 0
        best_value = -1000000
        best_move = valid_moves[0]
        for move in valid_moves:
            value = self.minimax(self.get_next_state(
                state, move), 1, False, alpha, beta)
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
        if isMaximizingPlayer:
            best_value = float('-inf')
            for move in valid_moves:
                value = self.minimax(self.get_next_state(
                    state, move), depth + 1, False, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(best_value, alpha)

                if beta <= alpha:
                    break

            return best_value
        # Minimizer
        else:
            best_value = float('inf')
            for move in valid_moves:
                value = self.minimax(self.get_next_state(
                    state, move), depth + 1, True, alpha, beta)
                best_value = min(best_value, value)
                beta = min(beta, best_value)

                if beta <= alpha:
                    break

            return best_value

    # Heuristic function to look at the board and evaluate its current value
    # this function will give 1 point for every chip the player has. Furthermore,
    # it will give an extra 5 points for every edge piece the player has and 10 points for a corner piece.
    def heuristic_eval(self, state):
        points = 0
        for x in range(0, 8):
            for y in range(0, 8):
                if (x == 0 or x == 7):
                    if (state.board[x][y] == state.turn):
                        points += 5
                elif (y == 0 or y == 7):
                    if (state.board[x][y] == state.turn):
                        points += 5
                if (state.board[x][y] == state.turn):
                    points += 1
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
