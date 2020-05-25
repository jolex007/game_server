import pygame

from game_object import GameObject


class FieldCell(GameObject):
    def __init__(self, x, y, w, h):
        GameObject.__init__(self, x, y, w, h)
        self.object = '.'
        pass

    def update(self):
        pass

    def draw(self, surface, is_curr_pos=False, is_selected_pos=False):
        new_bounds = pygame.rect.Rect(self.bounds.x - 1,
                                      self.bounds.y - 1,
                                      self.bounds.w + 2,
                                      self.bounds.h + 2)
        if is_selected_pos:
            pygame.draw.rect(surface, pygame.Color('magenta'), new_bounds)
        elif is_curr_pos:
            pygame.draw.rect(surface, pygame.Color('red'), new_bounds)
        if self.object == '.':
            pygame.draw.rect(surface, pygame.Color('green'), self.bounds)
        elif self.object == '@':
            pygame.draw.rect(surface, pygame.Color('yellow'), self.bounds)
        elif self.object == 'U':
            pygame.draw.rect(surface, pygame.Color('grey'), self.bounds)
        elif self.object == 'B':
            pygame.draw.rect(surface, pygame.Color('blue'), self.bounds)
        pass


class Field(GameObject):
    def __init__(self, x, y, w, size):
        GameObject.__init__(self, x, y, w, w)
        if (w + 1) % size != 0:
            raise Exception('Incorrect width of Field')

        self.field_size = size
        self.cell_width = ((w + 1) // size - 1)
        self.cells = [[FieldCell(x + i * (self.cell_width + 1),
                                 y + j * (self.cell_width + 1),
                                 self.cell_width, self.cell_width)
                       for j in range(size)] for i in range(size)]
        pass

    def update(self):
        for line in self.cells:
            for cell in line:
                cell.update()
        pass

    def move_unit(self, from_x, from_y, to_x, to_y):
        self.cells[from_x][from_y].object = '.'
        self.cells[to_x][to_y].object = 'U'

    def set_field(self, data):
        for x, row in enumerate(data):
            for y, elem in enumerate(row):
                self.cells[x][y].object = elem
        pass

    def get_cell(self, x, y):
        return self.cells[x][y].object

    def draw(self, surface, curr_pos, selected_pos):
        for x, line in enumerate(self.cells):
            for y, cell in enumerate(line):
                cell.draw(surface, is_curr_pos=((x, y) == curr_pos),
                          is_selected_pos=((x, y) == selected_pos))
        pass

    pass
