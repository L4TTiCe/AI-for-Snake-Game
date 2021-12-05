import pygame


class Theme:
    def __init__(self):
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)

    def get_gradient_modifier(self):
        return pygame.Color(0, 0, 0, 0)

    def get_board_color(self):
        return self.black

    def get_snake_color(self):
        return self.white

    def get_food_color(self):
        return self.red

    def get_grid_line_colors(self):
        return self.black


class Default(Theme):
    def __init__(self):
        super().__init__()

    def get_board_color(self):
        return pygame.Color(10, 49, 245)

    def get_snake_color(self):
        return pygame.Color(31, 240, 12)

    def get_food_color(self):
        return pygame.Color(250, 30, 30)

    def get_grid_line_colors(self):
        return pygame.Color(100, 100, 100)


class BlackTerror(Theme):
    def __init__(self):
        super().__init__()
        self.black = pygame.Color(0, 0, 0)
        self.battle_green = pygame.Color(121, 135, 83)
        self.red = pygame.Color(255, 0, 0)

    def get_board_color(self):
        return self.black

    def get_snake_color(self):
        return self.battle_green

    def get_food_color(self):
        return self.red

    def get_grid_line_colors(self):
        return self.black


class White(Theme):
    def __init__(self):
        super().__init__()

    def get_gradient_modifier(self):
        return pygame.Color(10, 5, 0, 5)

    def get_board_color(self):
        return self.white

    def get_snake_color(self):
        return pygame.Color(31, 240, 12)

    def get_food_color(self):
        return pygame.Color(250, 30, 30)

    def get_grid_line_colors(self):
        return pygame.Color(100, 100, 100)
