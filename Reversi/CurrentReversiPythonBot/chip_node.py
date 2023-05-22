
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

    #returns how deep children have been propigated
    def get_depth(self, depth=0):
        depth += 1
        if (len(self.children) != 0):
            return self.children[0].get_depth(depth)
        else:
            return depth
