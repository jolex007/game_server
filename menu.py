import pygame
from field import Field
from button import Button
import config as conf


class Menu:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

    pass


class MainMenu(Menu):
    def __init__(self, change_menu, exit_game):
        super().__init__()
        self.buttons = []
        self.change_menu = change_menu
        self.exit_game = exit_game
        self.state = 'Main'
        self.curr_pos = 0

        for i, (text, func) in enumerate((('Play', self.on_play),
                                          ('Quit', self.on_quit))):
            button = Button(conf.menu_offset_x,
                            conf.menu_offset_y + (conf.menu_button_h + 5) * i,
                            conf.menu_button_w,
                            conf.menu_button_h,
                            text,
                            func,
                            padding=5)
            self.buttons.append(button)

        pass

    def select_event(self):
        if self.curr_pos == 0:
            self.on_play()
        elif self.curr_pos == 1:
            self.on_quit()

    def get_event(self, event):
        if event.key == pygame.K_DOWN:
            self.curr_pos = (self.curr_pos + 1) % len(self.buttons)
        elif event.key == pygame.K_UP:
            self.curr_pos = (self.curr_pos - 1) % len(self.buttons)
        elif event.key == pygame.K_RETURN:
            self.select_event()
        pass

    def update(self, state='Main'):
        if self.state != state:
            if state == 'Stopped' or state == 'Play':
                self.buttons[0].set_text('Continue')
            elif state == 'Main':
                self.buttons[0].set_text('Play')
            self.state = state

        pass

    def draw(self, surface):
        for i, button in enumerate(self.buttons):
            if i == self.curr_pos:
                button.back_color = pygame.Color('Blue')
            else:
                button.back_color = pygame.Color('White')
            button.draw(surface)
        # TODO:
        pass

    def on_play(self):
        print('Play button pressed')
        self.state = 'Play'
        self.change_menu()
        pass

    def on_quit(self):
        print('Quit button pressed')
        self.exit_game()
        pass

    pass


class PlayMenu(Menu):
    def __init__(self, change_menu, send_command):
        super().__init__()
        self.change_menu = change_menu
        self.send_command = send_command
        self.curr_pos = (0, 0)
        self.selected_pos = (-1, -1)
        self.field = Field(conf.field_offset_x, conf.field_offset_y, conf.field_width, conf.field_size)
        pass

    def update(self):
        self.field.update()
        pass

    def select(self):
        if self.selected_pos == (-1, -1):
            self.selected_pos = self.curr_pos
        elif self.selected_pos == self.curr_pos:
            self.selected_pos = (-1, -1)
        else:
            # Move unit
            from_x, from_y = self.selected_pos
            to_x, to_y = self.curr_pos
            if self.field.get_cell(from_x, from_y) == '.' or \
                    self.field.get_cell(to_x, to_y) == 'U':
                return
            self.field.move_unit(from_x, from_y, to_x, to_y)
            command = 'move ' + str(from_x) + ' ' + str(from_y) + ' ' + \
                      str(to_x) + ' ' + str(to_y)
            self.send_command(command)
            self.selected_pos = (-1, -1)
        pass

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.field.draw(surface, self.curr_pos, self.selected_pos)
        # TODO: menu
        pass

    def hide(self):
        self.change_menu()
        pass

    def get_event(self, event):
        if event.key == pygame.K_UP:
            x, y = self.curr_pos
            self.curr_pos = (x, (y - 1) % conf.field_size)
        elif event.key == pygame.K_DOWN:
            x, y = self.curr_pos
            self.curr_pos = (x, (y + 1) % conf.field_size)
        elif event.key == pygame.K_LEFT:
            x, y = self.curr_pos
            self.curr_pos = ((x - 1) % conf.field_size, y)
        elif event.key == pygame.K_RIGHT:
            x, y = self.curr_pos
            self.curr_pos = ((x + 1) % conf.field_size, y)
        elif event.key == pygame.K_ESCAPE:
            self.hide()
        elif event.key == pygame.K_SPACE:
            self.select()
        pass

    pass
