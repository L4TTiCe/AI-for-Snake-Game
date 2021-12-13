from typing import List
import time

from game.Board import Board
from game.Coordinates import Coordinates
from pathtraversal.BoardWrapper import BoardWrapper
from pathtraversal.Statistics import Metric


class BFS:
    def __init__(self, board: Board, debug: bool):
        self.board = board

        self.visited: List[Coordinates] = []
        self.frontier: List[BoardWrapper] = []
        self.debug: bool = debug
        if self.debug:
            self.metrics: Metric = Metric()

    def find_path(self, destination: Coordinates):
        start_time = time.time()
        self.frontier.append(BoardWrapper(self.board, []))
        if self.debug:
            self.metrics.score = self.board.score
            self.metrics.turn = self.board.turn

        while len(self.frontier) > 0:
            curr_state = self.frontier.pop(0)
            if self.debug:
                self.metrics.nodes_expanded += 1

            if curr_state.board.snake.body[0] in self.visited:
                continue
            else:
                self.visited.append(curr_state.board.snake.body[0])

            curr_actions = curr_state.action
            curr_board = curr_state.board

            if curr_board.snake.body[0] == destination:
                exec_time = (time.time() - start_time)
                if self.debug:
                    self.metrics.time = exec_time
                    print("BFS: Flushing Metrics to file.")
                    self.metrics.flush_metric("bfs_stat.csv")
                # else:
                #     print(f"BFS Search succeeded in {exec_time}.")
                return curr_actions

            possible_actions = curr_board.possible_actions()

            for action in possible_actions:
                new_state = curr_board.get_successor_state(action)
                if new_state.snake.body[0] not in self.visited:
                    updated_actions: List[action] = curr_actions.copy()
                    updated_actions.append(action)
                    self.frontier.append(BoardWrapper(new_state, updated_actions))
