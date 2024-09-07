import pygame
from ParticleEffect import ParticleEffect

WIDTH, HEIGHT = 1910, 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
# Define particle effect classes for different events
class CoinExplosion(ParticleEffect):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW)
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)

class GemExplosion(ParticleEffect):
     def __init__(self, x, y):
        super().__init__(x, y, RED)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)

class KeyExplosion(ParticleEffect):
     def __init__(self, x, y):
        super().__init__(x, y, ORANGE)
        self.image = pygame.Surface((20, 20))
        self.image.fill(ORANGE)

class DestinationExplosion(ParticleEffect):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW)  # You can customize the color for destination explosion
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
# Define particle effect classes for wall collision and destination explosion
class WallExplosion(ParticleEffect):
    def __init__(self, x, y):
        super().__init__(x, y, RED)  
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)

