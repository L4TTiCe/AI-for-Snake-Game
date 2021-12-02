import pygame
import time

from game.GUI import GUI
from game.SnakeGame import SnakeGame
from pathtraversal.DFS import DFS


def process_game(game, view):
    game.check_collisions()
    view.redraw_window(game)
    view.event_handler()


def main():
    game = SnakeGame(10, loop_around=False)
    view = GUI()
    pygame.font.init()
    view.redraw_window(game)

    sleep_time = 0.2

    print(game.board)
    print("_____________________________________")
    traversal_agent = DFS(game.board)
    actions = traversal_agent.find_path()
    print(actions)

    for action in actions:
        # Reference:
        # https://stackoverflow.com/questions/20165492/pygame-window-not-responding-after-a-few-seconds
        pygame.event.get()
        view.redraw_window(game)
        game.move_snake(action)
        game.check_collision()
        print("--------------------------------------")
        print(game.board)
        time.sleep(sleep_time)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
