import math
import time
from heapq import heappush, heappop
from typing import List

from game.Actions import Actions
from game.Board import Board
from game.Coordinates import Coordinates
from pathtraversal.BoardWrapper import BoardWrapper
from pathtraversal.DFS import DFS
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


def get_blocked_nodes_count(board: Board):
    count: int = 0

    for rowIndex in range(board.rows):
        for colIndex in range(board.cols):
            current_coordinates: Coordinates = Coordinates(rowIndex, colIndex)
            if current_coordinates not in board.snake.body:
                traversal_agent = DFS(board, False)
                actions = traversal_agent.find_path(current_coordinates)

                if actions is None:
                    count += 1

    return count


def get_blocked_nodes_count_simplified(board: Board):
    count: int = 0

    for snake_part in board.snake.body:
        for action in [Actions.UP, Actions.RIGHT, Actions.DOWN, Actions.LEFT]:
            current_coordinates: Coordinates = snake_part.apply_modifier(action, board.loop_around, board.cols)
            if current_coordinates not in board.snake.body:
                traversal_agent = DFS(board, False)
                actions = traversal_agent.find_path(current_coordinates)

                if actions is None:
                    count += 1

    return count


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
    def __init__(self, board: Board, debug: bool):
        self.board = board

        self.visited: List[Coordinates] = []
        self.frontier = []
        self.counter: Counter = Counter()
        self.debug: bool = debug

        if self.debug:
            self.metrics: Metric = Metric()

    def find_path(self):
        start_time = time.time()

        # Priority Queue Reference:
        # https://docs.python.org/3/library/heapq.html
        heappush(self.frontier, (0, self.counter.get_count(), BoardWrapper(self.board, [])))

        if self.debug:
            self.metrics.score = self.board.score
            self.metrics.turn = self.board.turn

        while len(self.frontier) > 0:
            _, _, curr_state = heappop(self.frontier)
            if self.debug:
                self.metrics.nodes_expanded += 1

            if curr_state.board.snake.body[0] in self.visited:
                continue
            else:
                self.visited.append(curr_state.board.snake.body[0])

            curr_actions = curr_state.action
            curr_board = curr_state.board

            if curr_board.snake.body[0] == curr_board.fruit_pos:
                exec_time = (time.time() - start_time)
                if self.debug:
                    self.metrics.time = exec_time
                    print(f"AStar: Flushing Metrics to file. Search succeeded in {exec_time}.")
                    self.metrics.flush_metric("astar_manhattan_stat.csv")
                # else:
                #     print(f"A* Search succeeded in {exec_time}.")
                return curr_actions
            possible_actions = curr_board.possible_actions()

            for action in possible_actions:
                new_state = curr_board.get_successor_state(action)
                if new_state.snake.body[0] not in self.visited:
                    updated_actions: List[action] = curr_actions.copy()
                    updated_actions.append(action)
                    heuristic: int = manhattan_distance(new_state.snake.body[0], curr_board.fruit_pos, new_state) + get_blocked_nodes_count_simplified(new_state)
                    heappush(self.frontier, (heuristic, self.counter.get_count(), BoardWrapper(new_state, updated_actions)))
