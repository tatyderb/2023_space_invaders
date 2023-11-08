import pygame

from GUI.config import RSC, GEOM


class Application:

    def __init__(self):
        pygame.init()
        self.size = (self.width, self.height) = GEOM['display']

        self.FPS = RSC['FPS']
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption(RSC['title'])



    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                # нажали крестик на окне
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()


app = Application()
app.run()
