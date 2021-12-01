from enum import Enum

from game.Coordinates import Coordinates
from game.Directions import Directions


class States(Enum):
    NONE = "States.NONE",
    SNAKE_BODY = "States.SNAKE_BODY",
    SNAKE_HEAD = "States.SNAKE_HEAD",
    FOOD = "States.FOOD",


class BoardState:
    def __init__(self, state: States, direction: Directions):
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
        self.fruit_pos = Coordinates(0, 0)

        self.state = [[BoardState(States.NONE, Directions.NONE) for x in range(cols)] for y in range(rows)]

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
                    if self.state[row_index][col_index].direction == Directions.UP or self.state[row_index][
                        col_index].direction == Directions.DOWN:
                        output = output + " | "
                    else:
                        output = output + "---"
                else:
                    output = output + "   "
            output = output + "\n"
        return output

    def get_state_at(self, row: int, col: int):
        return self.state[row][col]

    def set_state_at(self, row: int, col: int, state: States, direction: Directions):
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
                direction: Directions = Directions.NONE
                if current_position_on_board == self.fruit_pos:
                    state = States.FOOD
                    direction = Directions.NONE
                    self.set_state_at(rowIndex, colIndex, state, direction)
                else:
                    self.set_state_at(rowIndex, colIndex, state, direction)
