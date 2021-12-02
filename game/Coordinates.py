from game.Actions import Actions


class Coordinates:
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y


    # Reference:
    # https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
    def __eq__(self, other):
        if isinstance(other, Coordinates):
            return self.x_coord == other.x_coord and self.y_coord == other.y_coord
        return False

    def apply_modifier(self, action: Actions):
        # print(direction)
        # match direction:
        #     case Actions.UP:
        #         return Coordinates(self.x_coord - 1, self.y_coord)
        #     case Actions.DOWN:
        #         return Coordinates(self.x_coord + 1, self.y_coord)
        #     case Actions.LEFT:
        #         return Coordinates(self.x_coord, self.y_coord - 1)
        #     case Actions.RIGHT:
        #         return Coordinates(self.x_coord, self.y_coord + 1)
        #     case Actions.NONE:
        #         return Coordinates(self.x_coord, self.y_coord)
        #     case _:
        #         print(direction)
        #         raise NotImplementedError
        if action.__str__() == "[<Actions.UP: 2>]" or action == Actions.UP:
            return Coordinates(self.x_coord - 1, self.y_coord)
        elif action.__str__() == "[<Actions.DOWN: 8>]" or action == Actions.DOWN:
            return Coordinates(self.x_coord + 1, self.y_coord)
        elif action.__str__() == "[<Actions.LEFT: 4>]" or action == Actions.LEFT:
            return Coordinates(self.x_coord, self.y_coord - 1)
        elif action.__str__() == "[<Actions.RIGHT: 6>]" or action == Actions.RIGHT:
            return Coordinates(self.x_coord, self.y_coord + 1)
        elif action.__str__() == "[<Actions.NONE: 5>]" or action == Actions.NONE:
            return Coordinates(self.x_coord, self.y_coord)
        else:
            # print(action.__str__())
            raise NotImplementedError

