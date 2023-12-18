""" Status bar для вывода что надо делать игроку / что делает противник."""
import pygame

from GUI.config import RSC, GEOM


class StatusBar:
    GAP = GEOM['ygap']
    def __init__(self, rect: pygame.Rect):
        self.rect = rect

        # TODO: пустая строка
        self.bgcolor = 'white'
        self.color = 'red'
        if RSC['status_bar']['font']:
            # TODO: взять фонт из файла
            raise('Not implemented yet.')
        else:
            self.font = pygame.font.SysFont(None, RSC['status_bar']['fontsize'])
        self.text = 'Вызов конструктора'
        self.y = self.rect.y + StatusBar.GAP

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value: str):
        print('Status bar: '+ value)
        self.__text = value
        self.img = self.font.render(value, True, self.color)
        w = self.img.get_width()
        h = self.img.get_height()
        self.x = int(self.rect.x + self.rect.width / 2 - w / 2)
        self.y = self.rect.y + StatusBar.GAP
        self.rect.height = h + 2 * StatusBar.GAP

    def draw(self, display: pygame.Surface):
        display.fill(self.bgcolor, self.rect)
        display.blit(self.img, (self.x, self.y))

