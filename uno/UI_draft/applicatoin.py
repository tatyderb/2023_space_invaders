import pygame

from UI_draft.game_view import GameView
from config import RSC, GEOM
from game import Game

FPS = RSC['FPS']


class Application:
    def __init__(self, filename: str | None = None):
        pygame.init()
        size = GEOM['display']
        self.display = pygame.display.set_mode(size)
        pygame.display.set_caption(RSC['title'])
        # icon_img = pygame.image.load(RSC['img']['icon'])
        # pygame.display.set_icon(icon_img)
        self.vgame = GameView(self.display.get_width(), self.display.get_height(), filename)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.vgame.redraw(self.display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.vgame.dispatcher(event)

            clock.tick(FPS)     # ждать 1/FPS секунды


if __name__ == '__main__':
    app = Application('data.json')
    app.run()
