import pygame

from config import RSC, GEOM

FPS = RSC['FPS']


class Application:
    def __init__(self):
        pygame.init()
        size = GEOM['display']
        self.display = pygame.display.set_mode(size)
        pygame.display.set_caption(RSC['title'])
        # icon_img = pygame.image.load(RSC['img']['icon'])
        # pygame.display.set_icon(icon_img)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(FPS)     # ждать 1/FPS секунды


if __name__ == '__main__':
    app = Application()
    app.run()