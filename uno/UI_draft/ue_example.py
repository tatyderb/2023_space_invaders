# Python program to add Custom Events
import pygame

pygame.init()

# Setting up the screen and timer
screen = pygame.display.set_mode((500, 500))
timer = pygame.time.Clock()

# set title
pygame.display.set_caption('Custom Events')

# defining colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Keep a track of active variable
bg_active_color = WHITE
screen.fill(WHITE)

# custom user event to change color
CHANGE_COLOR = pygame.USEREVENT + 1

# custom user event to inflate defalte
# box
ON_BOX = pygame.USEREVENT + 2

# creating Rectangle
box = pygame.Rect((225, 225, 50, 50))
grow = True

# posting a event to switch color after
# every 500ms
pygame.time.set_timer(CHANGE_COLOR, 500)

running = True
while running:

    # checks which all events are posted
    # and based on that perform required
    # operations
    for event in pygame.event.get():

        # switching colours after every
        # 500ms
        if event.type == CHANGE_COLOR:
            if bg_active_color == GREEN:
                screen.fill(GREEN)
                bg_active_color = WHITE
            elif bg_active_color == WHITE:
                screen.fill(WHITE)
                bg_active_color = GREEN

        if event.type == ON_BOX:

            # to inflate and deflate box
            if grow:
                box.inflate_ip(3, 3)
                grow = box.width < 75
            else:
                box.inflate_ip(-3, -3)
                grow = box.width < 50

        if event.type == pygame.QUIT:
            # for quitting the program
            running = False

    # Posting event when the cursor is on top
    # of the box
    if box.collidepoint(pygame.mouse.get_pos()):
        pygame.event.post(pygame.event.Event(ON_BOX))

        # Drawing rectangle on the screen
    pygame.draw.rect(screen, RED, box)

    # Updating Screen
    pygame.display.update()

    # Setting Frames per Second
    timer.tick(30)

pygame.quit()
