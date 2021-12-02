import pygame

from game.Actions import Actions
from game.GUI import GUI
from game.SnakeGame import SnakeGame
from game.Coordinates import Coordinates


def test_coordinates():
    test1: Coordinates = Coordinates(0,0)
    test2: Coordinates = Coordinates(0,0)
    print(test1 == test2)

    test1: Coordinates = Coordinates(5, 7)
    test2: Coordinates = Coordinates(5, 7)
    print(test1 == test2)

def test_coordinates_in_list():
    coords_list: list[Coordinates] = []

    coords_list.append(Coordinates(0,0))
    coords_list.append(Coordinates(0, 1))
    coords_list.append(Coordinates(0, 1))
    coords_list.append(Coordinates(0, 3))
    coords_list.append(Coordinates(0, 4))

    test1: Coordinates = Coordinates(0, 3)
    test2: Coordinates = Coordinates(5, 7)
    print(test1 in coords_list)


def main():
    test_coordinates()
    test_coordinates_in_list()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
