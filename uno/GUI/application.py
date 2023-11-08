import pygame

from GUI.config import RSC, GEOM
from GUI.game_view import ViewGame
from GUI.userevent import ANIMATION


class Application:

    def __init__(self):
        pygame.init()
        self.size = (self.width, self.height) = GEOM['display']

        self.FPS = RSC['FPS']
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(ANIMATION, int(1000 / self.FPS))

        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption(RSC['title'])

        self.vgame = ViewGame(self.size)

    def run(self):
        running = True
        while running:
            self.vgame.draw(self.display)
            for event in pygame.event.get():
                # нажали крестик на окне
                if event.type == pygame.QUIT:
                    running = False
                self.vgame.dispatcher(event)

        pygame.quit()


app = Application()
app.run()
