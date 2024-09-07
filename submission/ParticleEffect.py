import pygame
import random
# Define particle effect class for explosions
class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = random.randint(-5, 5)  # Random horizontal speed
        self.speed_y = random.randint(-5, 5)  # Random vertical speed
        self.lifetime = 20  # Number of frames the particle will exist

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
