
class Node:
    # requires on construction that the number of tiles occupied by the bot be
    # passed as the first parameter and the board of the state be passed as well.
    def __init__(self, points, turn, board, move=(0, 0)):
        self.points = points
        self.turn = turn
        self.board = board
        self.children = []
        self.move = move

    def insert_child(self, node):
        self.children.append(node)

    def get_child(self, index):
        if len(self.children) > index:
            return None
        return self.children[index]
