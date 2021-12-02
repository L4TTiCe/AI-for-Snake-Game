from game.Board import Board
from game.Actions import Actions
from typing import List


class BoardWrapper:
    def __init__(self, board: Board, actions: List[Actions]):
        self.board: Board = board
        self.action: List[actions] = actions


class BFS:

    def __init__(self, board: Board):
        self.board = board
        self.actions = []
        self.visited = []
        self.frontier: List[BoardWrapper] = []

    def bfs_path_traversal(self):
        self.frontier.append(BoardWrapper(self.board, []))
        while len(self.frontier) > 0:
            curr_state = self.frontier.pop()
            print(len(self.frontier))
            self.visited.append(self.board.snake.body[0])
            curr_actions = curr_state.action
            curr_board = curr_state.board
            if curr_board.snake.body[0] == curr_board.fruit_pos:
                return self.actions
            possible_actions = curr_board.possible_actions()
            print(curr_board)
            for action in possible_actions:
                new_state = curr_board.get_successor_state(action)
                for index in range(len(self.visited)):
                    if new_state.snake.body[0] != self.visited[index] and new_state.snake.body[0] != self.frontier:
                        updated_actions: List[action] = curr_actions.copy()
                        updated_actions.append(action)
                    # print(updated_actions)
                        self.frontier.append(BoardWrapper(new_state, updated_actions))






