import pygame

# Событие анимации, генерируется не чаще, чем наши FPS
ANIMATION = pygame.USEREVENT + 1

# конец полета
FLY_END = pygame.USEREVENT + 2

# нужен переход в следующую фазу игры (смена статуса game.status)
NEXT_PHASE = pygame.USEREVENT + 3

# Игра закончена
GAME_OVER = pygame.USEREVENT + 4

