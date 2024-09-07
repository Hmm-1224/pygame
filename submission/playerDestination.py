import pygame
CELL_SIZE = 40
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('player_robo.png').convert_alpha()
        scaled_width = int(CELL_SIZE * 1)
        scaled_height = int(CELL_SIZE * 1)
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def reduce_life(self):
        self.lives -= 1


# Destination class
class Destination(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('des.png').convert_alpha()
        scaled_width = int(CELL_SIZE * 1.1)
        scaled_height = int(CELL_SIZE * 1.1)
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


