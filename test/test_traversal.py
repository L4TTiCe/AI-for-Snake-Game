import random
import time

import pygame

from game.GUI import GUI
from game.SnakeGame import SnakeGame
from pathtraversal.DFS import DFS


def make_move(game, view, action):
    sleep_time = 0.2

    view.redraw_window(game)

    game.move_snake(action)
    game.check_collision()
    time.sleep(sleep_time)

    print("--------------------------------------")
    print(game.board)


def main():
    game = SnakeGame(6, loop_around=True)
    view = GUI()
    pygame.font.init()
    view.redraw_window(game)

    print(game.board)
    print("_____________________________________")

    while not game.is_game_over():
        # Reference:
        # https://stackoverflow.com/questions/20165492/pygame-window-not-responding-after-a-few-seconds
        pygame.event.get()

        traversal_agent = DFS(game.board)
        actions = traversal_agent.find_path()

        if actions is None:
            print(game.board.possible_actions())
            action = random.choice(list(game.board.possible_actions()))
            print(action)
            make_move(game, view, action)
        else:
            for action in actions:
                if not game.is_game_over():
                    make_move(game, view, action)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
