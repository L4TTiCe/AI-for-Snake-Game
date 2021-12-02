from game.Board import Board
from game.Actions import Actions
from game.Coordinates import Coordinates
from typing import List


class BoardWrapper:
    def __init__(self, board: Board, actions: List[Actions]):
        self.board: Board = board
        self.action: List[Actions] = actions


class DFS:

    def __init__(self, board: Board):
        self.board = board

        self.actions: List[Actions] = []
        self.visited: List[Coordinates] = []
        self.frontier: List[BoardWrapper] = []

    def find_path(self):
        self.frontier.append(BoardWrapper(self.board, []))

        while len(self.frontier) > 0:
            curr_state = self.frontier.pop()
            if curr_state.board.snake.body[0] in self.visited:
                continue
            else:
                self.visited.append(curr_state.board.snake.body[0])
                print(len(self.frontier))

            curr_actions = curr_state.action
            curr_board = curr_state.board

            if curr_board.snake.body[0] == curr_board.fruit_pos:
                print("Flag")
                return curr_actions
            possible_actions = curr_board.possible_actions()
            print(curr_board)

            for action in possible_actions:
                new_state = curr_board.get_successor_state(action)
                if new_state.snake.body[0] not in self.visited:
                    print(new_state.snake.body)
                    print(self.visited)
                    updated_actions: List[action] = curr_actions.copy()
                    updated_actions.append(action)
                    print(updated_actions)
                    self.frontier.append(BoardWrapper(new_state, updated_actions))






