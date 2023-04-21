import pygame
from GameFrame import RoomObject


class TextObject(RoomObject):
    def __init__(self, room, x, y, text='Not Set', size=60, font='PixelCode', colour=(0, 0, 0), bold=False, background = None):
        RoomObject.__init__(self, room, x, y)

        self.rendered_text = 0
        self.rect = 0
        self.built_font = 0
        self.text = text
        self.size = size
        self.font = font
        self.colour = colour
        self.bold = bold
        self.background = background
        self.update_text()

    def update_text(self):
        if self.font == 'PixelCode':
            self.built_font = pygame.font.Font("./fonts/PixelCode.otf", self.size)
        else:
            self.built_font = pygame.font.SysFont(self.font, self.size, self.bold)
        self.rendered_text = self.built_font.render(self.text, False, self.colour, self.background)
        self.image = self.rendered_text
        self.width, self.height = self.built_font.size(self.text)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_text_width(self):
        return self.built_font.size(self.text)[0]
