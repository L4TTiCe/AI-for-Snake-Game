import math
from heapq import heappush, heappop

from tqdm import tqdm

from game.Coordinates import Coordinates
from pathtraversal.BFS import BFS


class CoordinateDistanceWrapper:
    def __init__(self, coordinate: Coordinates, distance: int):
        self.position: Coordinates = coordinate
        self.cost = distance


class Counter:
    def __init__(self):
        self.count = 0

    def get_count(self):
        self.count += 1
        return self.count


def get_distance_deltas(board, end: Coordinates, start: Coordinates):
    x_distance = abs(start.x_coord - end.x_coord)
    y_distance = abs(start.y_coord - end.y_coord)
    if board.loop_around:
        if x_distance > board.rows:
            x_distance -= board.rows
        if y_distance > board.cols:
            y_distance -= board.cols
    return x_distance, y_distance


def manhattan_distance(start: Coordinates, end: Coordinates, board):
    # Reference:
    # https://stackoverflow.com/questions/3041366/shortest-distance-between-points-on-a-toroidally-wrapped-x-and-y-wrapping-ma
    x_distance, y_distance = get_distance_deltas(board, end, start)
    return x_distance + y_distance


def euclidean_distance(start: Coordinates, end: Coordinates, board):
    # Reference:
    # https://blog.demofox.org/2017/10/01/calculating-the-distance-between-points-in-wrap-around-toroidal-space/
    x_distance, y_distance = get_distance_deltas(board, end, start)
    return math.sqrt((x_distance * x_distance) + (y_distance * y_distance))


def get_fruit_pos(board):
    possible_options = []
    counter: Counter = Counter()

    for rowIndex in range(board.rows):
        for colIndex in range(board.cols):
            current_coordinates: Coordinates = Coordinates(rowIndex, colIndex)
            if current_coordinates not in board.snake.body:
                distance: int = manhattan_distance(board.snake.body[0], current_coordinates, board)
                coordinate_distance: CoordinateDistanceWrapper = CoordinateDistanceWrapper(current_coordinates,
                                                                                           distance)

                heappush(possible_options, (-distance, counter.get_count(), coordinate_distance))

    distance, _, coordinate_distance = heappop(possible_options)
    return coordinate_distance.position


def get_fruit_pos_bfs(board):
    possible_options = []
    counter: Counter = Counter()

    with tqdm(total=board.rows * board.cols) as pbar:
        for rowIndex in range(board.rows):
            for colIndex in range(board.cols):
                current_coordinates: Coordinates = Coordinates(rowIndex, colIndex)
                if current_coordinates not in board.snake.body:
                    traversal_agent = BFS(board, False)
                    actions = traversal_agent.find_path(current_coordinates)

                    if actions is None:
                        return current_coordinates
                    distance: int = len(actions)
                    coordinate_distance: CoordinateDistanceWrapper = CoordinateDistanceWrapper(current_coordinates,
                                                                                               distance)

                    heappush(possible_options, (-distance, counter.get_count(), coordinate_distance))
                pbar.update(1)

    distance, _, coordinate_distance = heappop(possible_options)
    return coordinate_distance.position
