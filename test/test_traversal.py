import pygame

from game.Actions import Actions
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

    print(game.board)
    print("_____________________________________")
    traversal_agent = DFS(game.board)
    actions = traversal_agent.find_path()
    print(actions)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
