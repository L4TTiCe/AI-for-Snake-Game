# **************************************************************************************
# Adapted from the work of [Craig Haber](https://github.com/craighaber) with the
# original work available at https://github.com/craighaber/AI-for-Snake-Game
# *************************************************************************************
import pygame

from game.Board import Actions
from game.GUI import Themes
from game.SnakeGame import SnakeGame


class GUIView:
    def __init__(self, theme=Themes.White()):
        self.width = 750
        self.height = 750
        self.grid_start_y = 30
        self.theme = theme
        self.win = pygame.display.set_mode((self.width, self.height))

    def redraw_window(self, game: SnakeGame):
        """Function to update the pygame window every frame, called from playSnakeGame.py."""

        # Board Tile color
        self.win.fill(self.theme.get_board_color())
        self.draw_data_window(game)
        self.draw_grid(game)
        self.draw_grid_updates(game)
        pygame.display.update()

    def draw_data_window(self, game: SnakeGame):
        """Function to draw the segment of the pygame window with the score and high score."""

        pygame.draw.rect(self.win, pygame.Color(50, 50, 50), (0, 0, self.width, self.grid_start_y))

        # Add the score and high score
        font = pygame.font.SysFont('calibri', 20)
        score_text = font.render('Score: ' + str(game.board.get_score()), 1, (255, 255, 255))
        self.win.blit(score_text, (10, 5))

    def draw_grid(self, game: SnakeGame):
        """Function to draw the grid in the pygame window where the game is played."""

        space_col = self.width // game.board.cols
        space_row = (self.height - self.grid_start_y) // game.board.rows

        for i in range(game.board.rows):
            # draw horizontal line
            pygame.draw.line(self.win, self.theme.get_grid_line_colors(), (0, space_row * i + self.grid_start_y),
                             (self.width, space_row * i + self.grid_start_y))

        for i in range(game.board.cols):
            # draw vertical line
            pygame.draw.line(self.win, self.theme.get_grid_line_colors(), (space_col * i, self.grid_start_y),
                             (space_col * i, self.height))

        # draw last lines so they are not cut off
        pygame.draw.line(self.win, self.theme.get_grid_line_colors(),
                         (space_col * game.board.rows - 2, self.grid_start_y),
                         (space_col * game.board.rows - 2, self.height))
        pygame.draw.line(self.win, self.theme.get_grid_line_colors(), (0, self.height - 2),
                         (self.width, self.height - 2))

    def draw_grid_updates(self, game: SnakeGame):
        """Function called from redraw_window() to update the grid area of the window."""

        space_col = self.width // game.board.cols
        space_row = (self.height - self.grid_start_y) // game.board.rows

        # Draw the fruit
        fruit_y = game.board.fruit_pos.x_coord
        fruit_x = game.board.fruit_pos.y_coord
        pygame.draw.rect(self.win, self.theme.get_food_color(), (
            space_col * fruit_x + 1, self.grid_start_y + space_row * fruit_y + 1, space_col - 1, space_row - 1))

        # Draw the updated snake since last movement
        for pos in game.board.snake.body:
            gradient_modifier = game.board.snake.body.index(pos)
            pos_y = pos.x_coord
            pos_x = pos.y_coord

            body_tile_color: pygame.Color = self.theme.get_snake_color()
            body_tile_color.update(
                min(255, body_tile_color.r + (self.theme.get_gradient_modifier().r * gradient_modifier)),
                min(255, body_tile_color.g + (self.theme.get_gradient_modifier().g * gradient_modifier)),
                min(255, body_tile_color.b + (self.theme.get_gradient_modifier().b * gradient_modifier)),
                max(100, body_tile_color.a - (self.theme.get_gradient_modifier().a * gradient_modifier))
            )
            pygame.draw.rect(self.win, body_tile_color, (
                space_col * pos_x + 1, self.grid_start_y + space_row * pos_y + 1, space_col - 1, space_row - 1))

        head = game.board.snake.body[0]
        head_y = head.x_coord
        head_x = head.y_coord
        try:
            head_dir = game.board.snake.directions[0]
        except IndexError:
            head_dir = Actions.DOWN

        # Draw eyes on the head of the snake, determining which direction they should face

        # if head facing left
        if head_dir == Actions.LEFT:
            # draw left eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + space_col // 10, self.grid_start_y + space_row * head_y + (space_row * 4) // 5), 2)
            # draw right eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + space_col // 10, self.grid_start_y + space_row * head_y + space_row // 5), 2)
        # if head facing up
        elif head_dir == Actions.UP:
            # draw left eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + space_col // 5, self.grid_start_y + space_row * head_y + space_row // 10), 2)
            # draw right eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + (space_col * 4) // 5, self.grid_start_y + space_row * head_y + space_row // 10), 2)
        # if head facing right
        elif head_dir == Actions.RIGHT:
            # draw left eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + (space_col * 9) // 10, self.grid_start_y + space_row * head_y + space_row // 5), 2)
            # draw right eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + (space_col * 9) // 10,
                self.grid_start_y + space_row * head_y + (space_row * 4) // 5),
                               2)
        # if head is facing down
        else:
            # draw left eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + space_col // 5, self.grid_start_y + space_row * head_y + (space_row * 9) // 10), 2)
            # draw right eye
            pygame.draw.circle(self.win, pygame.Color(100, 100, 100), (
                space_col * head_x + (space_col * 4) // 5,
                self.grid_start_y + space_row * head_y + (space_row * 9) // 10),
                               2)

    def event_handler(self):
        """Function for cleanly handling the event of the user quitting."""

        for event in pygame.event.get():
            # Check if user has quit the game
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                quit()
