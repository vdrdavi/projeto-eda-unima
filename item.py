import pygame
import random
import math

class Item:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.cor = (255, 215, 0)
        self.cor_borda = (255, 255, 0)
        self.coletado = False
        self.offset_y = 0
        self.tempo_animacao = random.uniform(0, 6.28)
        
    def update(self, dt):
        if not self.coletado:
            self.tempo_animacao += dt * 3
            self.offset_y = math.sin(self.tempo_animacao) * 3
    
    def draw(self, surface):
        if self.coletado:
            return
            
        pos_y = self.rect.y + self.offset_y
        rect_draw = pygame.Rect(self.rect.x, pos_y, self.rect.width, self.rect.height)
        pygame.draw.circle(surface, self.cor, rect_draw.center, 10)
        pygame.draw.circle(surface, self.cor_borda, rect_draw.center, 10, 2)
        pygame.draw.circle(surface, (255, 255, 255), rect_draw.center, 4)
    
    def coletar(self):
        self.coletado = True

