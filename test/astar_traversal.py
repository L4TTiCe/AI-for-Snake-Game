import random
import time

import pygame

from game.Actions import Actions
from game.GUI import Themes
from game.GUI.GUIView import GUIView
from game.SnakeGame import SnakeGame
from pathtraversal.A_star import AStar


def make_move(game, view, action):
    sleep_time = 0.2

    view.redraw_window(game)

    game.move_snake(action)
    game.check_collision()
    time.sleep(sleep_time)

    print("--------------------------------------")
    print(game.board)


def main():
    game = SnakeGame(7, loop_around=True)
    view = GUIView(Themes.White())
    pygame.font.init()
    view.redraw_window(game)

    print(game.board)
    print("_____________________________________")

    while not game.is_game_over():
        # Reference:
        # https://stackoverflow.com/questions/20165492/pygame-window-not-responding-after-a-few-seconds
        pygame.event.get()

        traversal_agent = AStar(game.board, True)
        actions = traversal_agent.find_path()

        if actions is None:
            print("Search Failed. ", end="")
            possible_actions = game.board.possible_actions()
            if possible_actions:
                print(f"Possible Actions: {game.board.possible_actions()}")
                print("Using Random: ", end='')
                action = random.choice(list(possible_actions))
            else:
                print("Using Random: ", end='')
                action = random.choice(list(Actions))
            print(action)
            make_move(game, view, action)
        else:
            for action in actions:
                pygame.event.get()
                if not game.is_game_over():
                    make_move(game, view, action)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
