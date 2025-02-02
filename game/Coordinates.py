from game.Actions import Actions


class Coordinates:
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y

    def __str__(self):
        return f"({self.x_coord}, {self.y_coord})"

    def __repr__(self):
        return "<Coordinates: %s>" % self

    # Reference:
    # https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
    def __eq__(self, other):
        if isinstance(other, Coordinates):
            return self.x_coord == other.x_coord and self.y_coord == other.y_coord
        return False

    def apply_modifier(self, action: Actions, loop_around: bool, size: int):
        match action:
            case Actions.UP:
                out_coords = Coordinates(self.x_coord - 1, self.y_coord)
            case Actions.DOWN:
                out_coords = Coordinates(self.x_coord + 1, self.y_coord)
            case Actions.LEFT:
                out_coords = Coordinates(self.x_coord, self.y_coord - 1)
            case Actions.RIGHT:
                out_coords = Coordinates(self.x_coord, self.y_coord + 1)
            case Actions.NONE:
                out_coords = Coordinates(self.x_coord, self.y_coord)
            case _:
                if action.__str__() == "[<Actions.UP: 2>]":
                    out_coords = Coordinates(self.x_coord - 1, self.y_coord)
                elif action.__str__() == "[<Actions.DOWN: 8>]":
                    out_coords = Coordinates(self.x_coord + 1, self.y_coord)
                elif action.__str__() == "[<Actions.LEFT: 4>]":
                    out_coords = Coordinates(self.x_coord, self.y_coord - 1)
                elif action.__str__() == "[<Actions.RIGHT: 6>]":
                    out_coords = Coordinates(self.x_coord, self.y_coord + 1)
                elif action.__str__() == "[<Actions.NONE: 5>]":
                    return Coordinates(self.x_coord, self.y_coord)
                else:
                    # print(action.__str__())
                    raise NotImplementedError

        if loop_around:
            if out_coords.x_coord == -1:
                out_coords.x_coord = size - 1
            elif out_coords.x_coord == size:
                out_coords.x_coord = 0

            if out_coords.y_coord == -1:
                out_coords.y_coord = size - 1
            elif out_coords.y_coord == size:
                out_coords.y_coord = 0

        return out_coords
