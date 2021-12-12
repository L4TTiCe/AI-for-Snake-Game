import collections
import copy
import random
from enum import Enum

from game.Actions import Actions
from game.Coordinates import Coordinates
from game.GameState import GameState
from game.agents.boardAgent import get_fruit_pos_bfs


class States(Enum):
    NONE = "States.NONE",
    SNAKE_BODY = "States.SNAKE_BODY",
    SNAKE_HEAD = "States.SNAKE_HEAD",
    FOOD = "States.FOOD",


class BoardState:
    def __init__(self, state: States, direction: Actions):
        self.state: States = state
        self.direction = direction

    def __str__(self):
        return self.state.name + " " + self.direction.name

    def __repr__(self):
        return "<BoardState: %s>" % self



# class CoordinateDistanceWrapper:
#     def __init__(self, coordinate: Coordinates, distance: int):
#         self.position: Coordinates = coordinate
#         self.cost = distance
#
#
# class Counter:
#     def __init__(self):
#         self.count = 0
#
#     def get_count(self):
#         self.count += 1
#         return self.count


class Board:
    def __init__(self, rows: int, cols: int, loop_around: bool, adversarial: bool):
        self.rows: int = rows
        self.cols: int = cols
        self.turn = 0
        self.loop_around: bool = loop_around
        self.adversarial: bool = adversarial
        self.snake = self.Snake()
        self.snake.body.append(Coordinates(self.rows // 2, self.cols // 2))
        self.game_state: GameState = GameState.INPROGRESS
        self.state = [[BoardState(States.NONE, Actions.NONE) for x in range(cols)] for y in range(rows)]
        self.score: int = 0
        self.fruit_pos: Coordinates = self.generate_fruit()
        self.update_board()

    def __str__(self):
        output = ""
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                if self.state[row_index][col_index].state == States.FOOD:
                    output = output + " F "
                elif self.state[row_index][col_index].state == States.SNAKE_HEAD:
                    output = output + " O "
                elif self.state[row_index][col_index].state == States.SNAKE_BODY:
                    # print(self.state[row_index][col_index].direction)
                    if self.state[row_index][col_index].direction == Actions.UP \
                            or self.state[row_index][col_index].direction == Actions.DOWN:
                        output = output + " | "
                    else:
                        output = output + "---"
                else:
                    output = output + "   "
            output = output + "\n"
        return output

    def check_collision(self):
        self.score += self.check_collisions()

    def get_score(self):
        return self.score

    def is_board_full(self):
        is_full: bool = True
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                if self.state[row_index][col_index].state == States.NONE:
                    is_full = False
                    return is_full
        if is_full:
            print("Board is Full! Ending Game.")
            self.game_state = GameState.OVER
            return is_full

    def generate_fruit(self):
        """Function to generate a new random position for the fruit."""
        if not self.is_board_full():
            if self.adversarial and self.turn != 0:
                return get_fruit_pos_bfs(self)
            fruit_pos: Coordinates = Coordinates(random.randrange(0, self.rows), random.randrange(0, self.cols))

            # Continually generate a location for the fruit until it is not in the snake's body
            while fruit_pos in self.snake.body:
                fruit_pos = Coordinates(random.randrange(0, self.rows), random.randrange(0, self.cols))

            return fruit_pos
        else:
            print(self)
            # raise LookupError

    def get_state_at(self, row: int, col: int):
        return self.state[row][col]

    def set_state_at(self, row: int, col: int, state: States, direction: Actions):
        self.state[row][col].state = state
        self.state[row][col].direction = direction

    def set_fruit_pos(self, fruit_pos: Coordinates):
        self.fruit_pos = fruit_pos
        self.update_board()

    def update_board(self):
        for rowIndex in range(self.rows):
            for colIndex in range(self.cols):
                current_position_on_board = Coordinates(rowIndex, colIndex)
                state: States = States.NONE
                direction: Actions = Actions.NONE
                if current_position_on_board == self.fruit_pos:
                    state = States.FOOD
                    direction = Actions.NONE
                    self.set_state_at(rowIndex, colIndex, state, direction)
                elif current_position_on_board in self.snake.body:
                    state = States.SNAKE_BODY
                    head = self.snake.body[0]
                    if current_position_on_board == head:
                        state = States.SNAKE_HEAD
                    index = self.snake.body.index(current_position_on_board)
                    try:
                        direction = self.snake.directions.__getitem__(index)
                    except IndexError:
                        direction = Actions.NONE
                    self.set_state_at(rowIndex, colIndex, state, direction)
                else:
                    self.set_state_at(rowIndex, colIndex, state, direction)

    def check_collisions(self):
        """Function that consecutively calls all the functions that detect collisions."""

        score = self.check_fruit_collision()
        self.check_wall_collision()
        self.check_body_collision()
        return score

    def check_fruit_collision(self):
        """Function that detects and handles if the snake has collided with a fruit."""
        # If we found a fruit
        if self.snake.body[0] == self.fruit_pos:
            # Add the new body square to the tail of the snake
            self.extend_snake()
            # Generate a new fruit in a random position
            self.set_fruit_pos(self.generate_fruit())
            self.update_board()
            return 1
        else:
            return 0

    def check_wall_collision(self):
        """Function that checks and handles if the snake has collided with a wall."""

        # Only need to check the collisions of the head of the snake
        head = self.snake.body[0]
        head_y = head.y_coord
        head_x = head.x_coord

        # If there is a wall collision, game over
        if head_x == self.cols or head_y == self.rows or head_x < 0 or head_y < 0:
            print("Collision. Game Over.")
            self.game_state = GameState.OVER

    def check_body_collision(self):
        """Function that checks and handles if the snake has collided with its own body."""

        if len(self.snake.body) > 1:
            # Only need to check the collisions of the head of the snake
            head = self.snake.body[0]
            body_without_head = self.snake.body[1:]
            if head in body_without_head:
                print("Self-Collision. Game Over.")
                self.game_state = GameState.OVER

    def update_body_positions(self):
        """
        Updates the snake's body positions.

        The snake's body positions are updated based on the directions in
        self.directions. This update occurs each frame, and is called directly
        from all the classes that run the Snake Game.
        """
        # Iterate through each square that is part of the snake's body
        for i, pos in enumerate(self.snake.body):
            # Get the direction to move next that corresponds to the body position
            direction = self.snake.directions[i]
            # Update the body position after moving in the direction
            updated_pos = pos.apply_modifier(direction, self.loop_around, self.rows)

            self.snake.body[i] = updated_pos
            self.update_board()

    def extend_snake(self):
        """
        Adds one extra block to the end of the snake's body.

        This function is called directly from the
        SnakeGame class whenever the snake eats a fruit.
        """
        snake_tail = self.snake.body[-1]
        # Get the direction of the tail of the body
        tail_dir = self.snake.directions[-1]

        # spawn the new body component in the opposite direction of the snake's movement
        match tail_dir:
            case Actions.DOWN:
                self.snake.body.append(snake_tail.apply_modifier(Actions.UP, self.loop_around, self.rows))
            case Actions.UP:
                self.snake.body.append(snake_tail.apply_modifier(Actions.DOWN, self.loop_around, self.rows))
            case Actions.LEFT:
                self.snake.body.append(snake_tail.apply_modifier(Actions.RIGHT, self.loop_around, self.rows))
            case Actions.RIGHT:
                self.snake.body.append(snake_tail.apply_modifier(Actions.LEFT, self.loop_around, self.rows))
            case _:
                # print(tail_dir)
                if tail_dir.__str__() == "[<Actions.UP: 2>]":
                    self.snake.body.append(snake_tail.apply_modifier(Actions.DOWN, self.loop_around, self.rows))
                elif tail_dir.__str__() == "[<Actions.DOWN: 8>]":
                    self.snake.body.append(snake_tail.apply_modifier(Actions.UP, self.loop_around, self.rows))
                elif tail_dir.__str__() == "[<Actions.LEFT: 4>]":
                    self.snake.body.append(snake_tail.apply_modifier(Actions.RIGHT, self.loop_around, self.rows))
                elif tail_dir.__str__() == "[<Actions.RIGHT: 6>]":
                    self.snake.body.append(snake_tail.apply_modifier(Actions.LEFT, self.loop_around, self.rows))
                elif tail_dir.__str__() == "[<Actions.NONE: 5>]":
                    raise NotImplementedError
                else:
                    # print(action.__str__())
                    raise LookupError
        self.update_board()

        # This functions returns a list of directions that the snake can take after the current position

    def possible_actions(self):
        """This function returns the possible set of moves that the snake can take from the current position"""
        snake_head: Coordinates = self.snake.body[0]
        possible_movement: list[(Coordinates, Actions)] = [
            (snake_head.apply_modifier(Actions.UP, self.loop_around, self.rows), Actions.UP),
            (snake_head.apply_modifier(Actions.RIGHT, self.loop_around, self.rows), Actions.RIGHT),
            (snake_head.apply_modifier(Actions.LEFT, self.loop_around, self.rows), Actions.LEFT),
            (snake_head.apply_modifier(Actions.DOWN, self.loop_around, self.rows), Actions.DOWN)]

        possible_actions: list[Actions] = []

        for coords, action in possible_movement:
            if not self.loop_around:
                if 0 <= coords.x_coord <= self.rows - 1 and 0 <= coords.y_coord <= self.cols - 1:
                    if self.get_state_at(coords.x_coord, coords.y_coord).state == States.NONE \
                            or self.get_state_at(coords.x_coord, coords.y_coord).state == States.FOOD:
                        possible_actions.append(action)
            else:
                if self.get_state_at(coords.x_coord, coords.y_coord).state == States.NONE \
                        or self.get_state_at(coords.x_coord, coords.y_coord).state == States.FOOD:
                    possible_actions.append(action)

        return possible_actions

    def move(self, action: Actions):
        self.turn += 1
        self.snake.directions.appendleft(action)
        if len(self.snake.directions) > len(self.snake.body):
            self.snake.directions.pop()
        self.update_body_positions()

    def get_successor_state(self, action: Actions):
        new_state = copy.deepcopy(self)
        new_state.move(action)
        return new_state

    class Snake:
        def __init__(self):
            """Initializes Snake class"""
            self.body: list[Coordinates] = []
            self.directions = collections.deque()

# def get_distance_deltas(board: Board, end: Coordinates, start: Coordinates):
#     x_distance = abs(start.x_coord - end.x_coord)
#     y_distance = abs(start.y_coord - end.y_coord)
#     if board.loop_around:
#         if x_distance > board.rows:
#             x_distance -= board.rows
#         if y_distance > board.cols:
#             y_distance -= board.cols
#     return x_distance, y_distance
#
#
# def manhattan_distance(start: Coordinates, end: Coordinates, board: Board):
#     # Reference:
#     # https://stackoverflow.com/questions/3041366/shortest-distance-between-points-on-a-toroidally-wrapped-x-and-y-wrapping-ma
#     x_distance, y_distance = get_distance_deltas(board, end, start)
#     return x_distance + y_distance
#
#
# def euclidean_distance(start: Coordinates, end: Coordinates, board: Board):
#     # Reference:
#     # https://blog.demofox.org/2017/10/01/calculating-the-distance-between-points-in-wrap-around-toroidal-space/
#     x_distance, y_distance = get_distance_deltas(board, end, start)
#     return math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
#
#
# def get_fruit_pos(board: Board):
#     possible_options = []
#     counter: Counter = Counter()
#
#     for rowIndex in range(board.rows):
#         for colIndex in range(board.cols):
#             current_coordinates: Coordinates = Coordinates(rowIndex, colIndex)
#             if current_coordinates not in board.snake.body:
#                 distance: int = manhattan_distance(board.snake.body[0], current_coordinates, board)
#                 coordinate_distance: CoordinateDistanceWrapper = CoordinateDistanceWrapper(current_coordinates,
#                                                                                            distance)
#
#                 heappush(possible_options, (-distance, counter.get_count(), coordinate_distance))
#
#     distance, _, coordinate_distance = heappop(possible_options)
#     return coordinate_distance.position