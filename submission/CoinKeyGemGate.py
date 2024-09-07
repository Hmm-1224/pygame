import pygame
CELL_SIZE = 40
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('coin.png').convert_alpha()
        scaled_width = int(CELL_SIZE * 1)
        scaled_height = int(CELL_SIZE * 1)
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('key.png').convert_alpha()
        scaled_width = int(CELL_SIZE * 1)
        scaled_height = int(CELL_SIZE * 1)
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('gate.png').convert_alpha()
        scaled_width = int(CELL_SIZE * 1)
        scaled_height = int(CELL_SIZE * 1)
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('gem.png').convert_alpha()
        scaled_width = int(CELL_SIZE * 1)
        scaled_height = int(CELL_SIZE * 1)
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)        
