import pygame

from GUI.config import RSC, GEOM
from GUI.game_view import ViewGame
from GUI.userevent import NEXT_PHASE
from game import Game


class Application:

    def __init__(self, filename: str | None = None):
        pygame.init()
        self.size = (self.width, self.height) = GEOM['display']

        self.FPS = RSC['FPS']
        self.clock = pygame.time.Clock()

        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption(RSC['title'])

        # if filename:
        #     self.vgame = ViewGame.create(filename)
        # else:
        #     self.vgame = ViewGame(self.size)
        self.vgame = ViewGame(self.size, Game(['Bob', 'Mike']))

    def run(self):
        running = True
        pygame.event.post(pygame.event.Event(NEXT_PHASE))

        while running:
            self.vgame.draw(self.display)
            for event in pygame.event.get():
                # нажали крестик на окне
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    self.vgame = ViewGame(self.size, Game(['Bob', 'Mike']))
                else:
                    self.vgame.dispatcher(event)

        pygame.quit()


# пока никаких случайностей
import random
random.seed(7)

app = Application()
app.run()
