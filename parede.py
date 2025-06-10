import pygame

class Parede:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (211, 211, 211)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
