import pygame
import math

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = (80, 200, 120)
        self.speed = 400

    def update(self, keys, dt):
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        if dx != 0 or dy != 0:
            magnitude = math.sqrt(dx * dx + dy * dy)
            dx = dx / magnitude
            dy = dy / magnitude

        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

