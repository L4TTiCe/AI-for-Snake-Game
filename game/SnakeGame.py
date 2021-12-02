# **************************************************************************************
# Adapted from the work of [Craig Haber](https://github.com/craighaber) with the
# original work available at https://github.com/craighaber/AI-for-Snake-Game
# *************************************************************************************
import copy
from game.Board import Board, States
from game.Actions import Actions
from game.GameState import GameState


class SnakeGame:

    def __init__(self, size: int, loop_around):
        """Initializes the SnakeGame class."""
        self.board = Board(size, size, loop_around)

    def move_snake(self, action: Actions):
        """Function to allow the user to move the snake with the arrow keys."""
        if not self.is_game_over():
            self.board.move(action)
        else:
            raise RuntimeError

    def is_game_over(self):
        if self.board.game_state == GameState.INPROGRESS:
            return False
        else:
            return True

    def get_board(self):
        self.board.update_board()
        return self.board

    def check_collision(self):
        self.board.check_collision()

    # This functions returns a list of directions that the snake can take after the current position
    def possible_moves(self):
        """This function returns the possible set of moves that the snake can take from the current position"""
        snake_head = self.board.snake.body[0]
        # A list of the coordinates around the snake and the direction possible
        coordinates_around = []
        # Snake's head x-coordinate
        snake_x_coordinate = snake_head.x_coord
        # Snake's head y-coordinate
        snake_y_coordinate = snake_head.y_coord
        # Gets the current board state
        current_board_state = self.get_board()
        final_coordinates_around = []
        # Append the coordinates possible around the board
        coordinates_around.append([snake_x_coordinate + 1, snake_y_coordinate, Actions.DOWN])
        coordinates_around.append([snake_x_coordinate, snake_y_coordinate + 1, Actions.RIGHT])
        coordinates_around.append([snake_x_coordinate - 1, snake_y_coordinate, Actions.UP])
        coordinates_around.append([snake_x_coordinate, snake_y_coordinate - 1, Actions.LEFT])
        # If loop_around is false
        for x, y, direction in coordinates_around:
            if not self.board.loop_around:
                if 0 <= x <= self.board.rows - 1 and 0 <= y <= self.board.cols - 1:
                    if current_board_state.get_state_at(x, y).state == States.NONE \
                            or current_board_state.get_state_at(x, y).state == States.FOOD:
                        final_coordinates_around.append([x, y, direction])
            else:
                # If loop around is true
                coordinates = snake_head.apply_modifier(direction)
                x = coordinates.x_coord
                y = coordinates.y_coord
                if current_board_state.get_state_at(x, y).state == States.NONE:
                    final_coordinates_around.append([x, y, direction])

        # print(final_coordinates_around)

    def get_successor_state(self, action: Actions):
        return self.board.get_successor_state(action)
