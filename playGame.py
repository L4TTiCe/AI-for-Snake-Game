import time

import keyboard  # using module keyboard
import pygame

from game.Board import Actions
from game.GUI import Themes
from game.GUI.GUIView import GUIView
from game.SnakeGame import SnakeGame


def make_move(game, view, action):
    sleep_time = 0.2

    game.move_snake(action)
    game.check_collision()
    view.redraw_window(game)
    time.sleep(sleep_time)


# Uses keyboard (python module) to directly query for key presses, without relying on the console inputs.
def play_game():
    game = SnakeGame(10, loop_around=Themes)
    view = GUIView()
    pygame.font.init()
    view.redraw_window(game)

    # Reference:
    # https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
    while not game.is_game_over():  # making a loop
        # Reference:
        # https://stackoverflow.com/questions/20165492/pygame-window-not-responding-after-a-few-seconds
        pygame.event.get()
        if keyboard.is_pressed('w'):  # if key 'q' is pressed
            make_move(game, view, Actions.UP)
        if keyboard.is_pressed('s'):
            make_move(game, view, Actions.DOWN)
        if keyboard.is_pressed('a'):
            make_move(game, view, Actions.LEFT)
        if keyboard.is_pressed('d'):
            make_move(game, view, Actions.RIGHT)

        view.event_handler()

    print(f'Game Over. You Scored: {game.board.get_score()}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    play_game()
