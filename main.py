import pygame

from game.Board import Actions
from game.GUI import GUI
from game.SnakeGame import SnakeGame


def main():
    # size = int(input("Enter the size of the board: "))
    game = SnakeGame(10, loop_around=False)
    view = GUI()
    pygame.font.init()
    view.redraw_window(game)

    while not game.is_game_over():
        print(game.get_board())
        print(f'Score: {game.board.get_score()}')
        token = input("Move: ")
        match token:
            case "w":
                game.move_snake(Actions.UP)
            case "s":
                game.move_snake(Actions.DOWN)
            case "a":
                game.move_snake(Actions.LEFT)
            case "d":
                game.move_snake(Actions.RIGHT)
            case _:
                print("Invalid token use WSAD")

        game.board.check_collisions()
        game.board.possible_actions()
        view.redraw_window(game)
        view.event_handler()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
