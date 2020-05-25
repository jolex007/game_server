import pygame


class TextField:
    def __init__(self, x, y, text_func, color, font_name, font_size):
        self.pos = (x, y)
        self.text = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface()
        pass

    def get_surface(self):
        text_surface = self.font.render(self.text(), False, self.color)
        return text_surface, text_surface.get_rect()
        pass

    def update(self):
        pass

    def draw(self, surface):
        text_surface, self.bounds = self.get_surface()
        pos = self.pos
        surface.blit(text_surface, pos)
        pass
    pass
