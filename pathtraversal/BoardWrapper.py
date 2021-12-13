from typing import List

from game.Actions import Actions
# from game.Board import Board


class BoardWrapper:
    def __init__(self, board, actions: List[Actions]):
        self.board = board
        self.action: List[Actions] = actions
