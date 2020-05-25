import pygame
import sys

from menu import MainMenu, PlayMenu
from web_module import WebModule
from _thread import start_new_thread


class Game:
    def __init__(self, caption, width, height):
        pygame.init()
        pygame.font.init()

        self.main_menu = MainMenu(self.change_menu, self.exit_game)
        self.play_menu = PlayMenu(self.change_menu, self.send_command)
        self.web = WebModule(self.ready_to_play, self.play_menu.field.set_field)
        self.status = 'Main'

        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

        pass

    def update(self):
        if self.status == 'Main':
            self.main_menu.update(self.status)
        elif self.status == 'Play':
            self.play_menu.update()
        elif self.status == 'Stopped':
            self.main_menu.update(self.status)

    def draw(self):
        if self.status == 'Main':
            self.main_menu.draw(self.surface)
        elif self.status == 'Play':
            self.play_menu.draw(self.surface)
        elif self.status == 'Stopped':
            self.main_menu.draw(self.surface)

    def send_command(self, command):
        self.web.send_command(command)
        pass

    def send_event(self, event):
        if self.status == 'Main' or self.status == 'Stopped':
            self.main_menu.get_event(event)
        else:
            self.play_menu.get_event(event)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # TODO: Send on socket
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                self.send_event(event)
        pass

    def connect(self):
        start_new_thread(self.web.start, ())
        pass

    def ready_to_play(self):
        self.status = 'Play'
        pass

    def change_menu(self):
        print(self.status)
        self.surface.fill((0, 0, 0))
        if self.status == 'Main':
            self.status = 'Waiting'
            self.connect()
        elif self.status == 'Play':
            self.status = 'Stopped'
        elif self.status == 'Stopped':
            self.status = 'Play'
        pass

    def exit_game(self):
        pygame.quit()
        sys.exit()
        pass

    def run(self):
        while self.status != 'Exit':
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
        pass
    pass
