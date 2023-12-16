import pygame

from GUI.config import RSC, GEOM
from GUI.game_view import ViewGame
from GUI.userevent import ANIMATION


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
        self.vgame = ViewGame(self.size)

    def run(self):
        running = True
        while running:
            self.vgame.model_update()
            self.vgame.draw(self.display)
            for event in pygame.event.get():
                # нажали крестик на окне
                if event.type == pygame.QUIT:
                    running = False
                self.vgame.dispatcher(event)

        pygame.quit()


app = Application('../test/save1.json')
app.run()
