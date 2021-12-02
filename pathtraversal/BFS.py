from typing import List

from game.Board import Board
from game.Coordinates import Coordinates
from pathtraversal.BoardWrapper import BoardWrapper


class BFS:
    def __init__(self, board: Board):
        self.board = board

        self.visited: List[Coordinates] = []
        self.frontier: List[BoardWrapper] = []

    def find_path(self):
        self.frontier.append(BoardWrapper(self.board, []))

        while len(self.frontier) > 0:
            curr_state = self.frontier.pop(0)
            if curr_state.board.snake.body[0] in self.visited:
                continue
            else:
                self.visited.append(curr_state.board.snake.body[0])

            curr_actions = curr_state.action
            curr_board = curr_state.board

            if curr_board.snake.body[0] == curr_board.fruit_pos:
                return curr_actions
            possible_actions = curr_board.possible_actions()

            for action in possible_actions:
                new_state = curr_board.get_successor_state(action)
                if new_state.snake.body[0] not in self.visited:
                    updated_actions: List[action] = curr_actions.copy()
                    updated_actions.append(action)
                    self.frontier.append(BoardWrapper(new_state, updated_actions))
