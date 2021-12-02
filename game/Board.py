import collections
from enum import Enum
import random

from game.Coordinates import Coordinates
from game.Actions import Actions
from game.GameState import GameState

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


class Board:
    def __init__(self, rows: int, cols: int, loop_around: bool):
        self.rows: int = rows
        self.cols: int = cols
        self.loop_around = loop_around
        self.snake = self.Snake()
        self.snake.body.append(self.initialize_snake())
        self.fruit_pos = self.generate_fruit()
        self.game_state = GameState.INPROGRESS
        self.state = [[BoardState(States.NONE, Actions.NONE) for x in range(cols)] for y in range(rows)]
        self.score = 0

    def __str__(self):
        output = ""
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                if self.state[row_index][col_index].state == States.FOOD:
                    output = output + " F "
                elif self.state[row_index][col_index].state == States.SNAKE_HEAD:
                    output = output + " O "
                elif self.state[row_index][col_index].state == States.SNAKE_BODY:
                    print(self.state[row_index][col_index].direction)
                    if self.state[row_index][col_index].direction == Actions.UP or self.state[row_index][
                        col_index].direction == Actions.DOWN:
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

    def generate_fruit(self):
        """Function to generate a new random position for the fruit."""
        fruit_pos = Coordinates(random.randrange(0, self.rows), random.randrange(0, self.cols))

        # Continually generate a location for the fruit until it is not in the snake's body
        while fruit_pos in self.snake.body:
            fruit_pos = Coordinates(random.randrange(0, self.rows), random.randrange(0, self.cols))

        return fruit_pos

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
            self.game_state = GameState.OVER

    def check_body_collision(self):
        """Function that checks and handles if the snake has collided with its own body."""

        if len(self.snake.body) > 1:
            # Only need to check the collisions of the head of the snake
            head = self.snake.body[0]
            body_without_head = self.snake.body[1:]
            if head in body_without_head:
                self.game_state = GameState.OVER

    def initialize_snake(self):
        """
        Initializes the first position for the snake.

        Returns:
        A Coordinate representing the position for the snake.

        """
        snake_row = self.rows // 2
        snake_col = self.cols // 2

        return Coordinates(snake_row, snake_col)

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
            updated_pos = pos.apply_modifier(direction)

            # Loop around logic
            if self.loop_around:
                if updated_pos.x_coord == -1:
                    updated_pos.x_coord = self.rows - 1
                elif updated_pos.x_coord == self.rows:
                    updated_pos.x_coord = 0

                if updated_pos.y_coord == -1:
                    updated_pos.y_coord = self.rows - 1
                elif updated_pos.y_coord == self.cols:
                    updated_pos.y_coord = 0

            self.snake.body[i] = updated_pos
            self.update_snake_board()

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
                self.snake.body.append(snake_tail.apply_modifier(Actions.UP))
            case Actions.UP:
                self.snake.body.append(snake_tail.apply_modifier(Actions.DOWN))
            case Actions.LEFT:
                self.snake.body.append(snake_tail.apply_modifier(Actions.RIGHT))
            case Actions.RIGHT:
                self.snake.body.append(snake_tail.apply_modifier(Actions.LEFT))
            case _:
                raise LookupError
        self.update_snake_board()

    def update_snake_board(self):

        for rowIndex in range(self.rows):
            for colIndex in range(self.cols):
                current_position_on_board = Coordinates(rowIndex, colIndex)
                state: States = States.NONE
                direction: Actions = Actions.NONE

                if current_position_on_board in  self.snake.body:
                    state = States.SNAKE_BODY
                    head =  self.snake.body[0]
                    if current_position_on_board == head:
                        state = States.SNAKE_HEAD

                    index = self.snake.body.index(current_position_on_board)
                    try:
                        direction = self.snake.directions.__getitem__(index)
                    except IndexError:
                        direction = Actions.NONE
                    self.set_state_at(rowIndex, colIndex, state, direction)

    class Snake:
        def __init__(self):
            """Initializes Snake class"""
            self.body = []
            self.directions = collections.deque()