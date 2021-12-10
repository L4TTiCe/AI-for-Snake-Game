import math
from heapq import heappush, heappop
from typing import List

from game.Board import Board
from game.Coordinates import Coordinates
from pathtraversal.BoardWrapper import BoardWrapper
from pathtraversal.Statistics import Metric


def manhattan_distance(start: Coordinates, end: Coordinates, board: Board):
    # Reference:
    # https://stackoverflow.com/questions/3041366/shortest-distance-between-points-on-a-toroidally-wrapped-x-and-y-wrapping-ma
    x_distance, y_distance = get_distance_deltas(board, end, start)
    return x_distance + y_distance


def euclidean_distance(start: Coordinates, end: Coordinates, board: Board):
    # Reference:
    # https://blog.demofox.org/2017/10/01/calculating-the-distance-between-points-in-wrap-around-toroidal-space/
    x_distance, y_distance = get_distance_deltas(board, end, start)
    return math.sqrt((x_distance * x_distance) + (y_distance * y_distance))


def get_distance_deltas(board: Board, end: Coordinates, start: Coordinates):
    x_distance = abs(start.x_coord - end.x_coord)
    y_distance = abs(start.y_coord - end.y_coord)
    if board.loop_around:
        if x_distance > board.rows:
            x_distance -= board.rows
        if y_distance > board.cols:
            y_distance -= board.cols
    return x_distance, y_distance


class Counter:
    def __init__(self):
        self.count = 0

    def get_count(self):
        self.count += 1
        return self.count


class AStar:
    def __init__(self, board: Board):
        self.board = board

        self.visited: List[Coordinates] = []
        self.frontier = []
        self.counter: Counter = Counter()
        self.metrics: Metric = Metric()

    def find_path(self):
        # Priority Queue Reference:
        # https://docs.python.org/3/library/heapq.html
        heappush(self.frontier, (0, self.counter.get_count(), BoardWrapper(self.board, [])))
        self.metrics.score = self.board.score
        self.metrics.turn = self.board.turn

        while len(self.frontier) > 0:
            _, _, curr_state = heappop(self.frontier)
            self.metrics.nodes_expanded += 1

            if curr_state.board.snake.body[0] in self.visited:
                continue
            else:
                self.visited.append(curr_state.board.snake.body[0])

            curr_actions = curr_state.action
            curr_board = curr_state.board

            if curr_board.snake.body[0] == curr_board.fruit_pos:
                print("Flushing Metrics to file.")
                self.metrics.flush_metric("astar_manhattan_stat.csv")
                return curr_actions
            possible_actions = curr_board.possible_actions()

            for action in possible_actions:
                new_state = curr_board.get_successor_state(action)
                if new_state.snake.body[0] not in self.visited:
                    updated_actions: List[action] = curr_actions.copy()
                    updated_actions.append(action)
                    heappush(self.frontier, (
                        manhattan_distance(new_state.snake.body[0], curr_board.fruit_pos, new_state),
                        self.counter.get_count(), BoardWrapper(new_state, updated_actions)))
