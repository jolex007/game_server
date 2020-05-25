import pygame

from game_object import GameObject
from text_object import TextField
import config as conf


class Button(GameObject):
    def __init__(self, x, y, w, h, text, func_click=lambda x: None, padding=0):
        super().__init__(x, y, w, h)
        self.state = 'normal'
        self.func_click = func_click
        self.back_color = pygame.Color('White')

        self.text = TextField(x + padding,
                              y + padding,
                              lambda: text,
                              conf.button_text_color,
                              conf.font_name,
                              conf.font_size)
        pass

    def set_text(self, text):
        self.text.text = lambda: text
        pass

    def draw(self, surface):
        pygame.draw.rect(surface,
                         self.back_color,
                         self.bounds)
        self.text.draw(surface)
        pass

    pass
