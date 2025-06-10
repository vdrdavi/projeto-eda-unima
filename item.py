import pygame
import random
import math

class Item:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.cor = (255, 215, 0)  # Dourado
        self.cor_borda = (255, 255, 0)  # Amarelo
        self.coletado = False  # IMPORTANTE: adicionar este atributo
        
        # Animação de flutuação
        self.offset_y = 0
        self.tempo_animacao = random.uniform(0, 6.28)  # Começar em pontos diferentes da animação
        
    def update(self, dt):
        """Atualiza a animação do item"""
        if not self.coletado:
            self.tempo_animacao += dt * 3  # Velocidade da flutuação
            self.offset_y = math.sin(self.tempo_animacao) * 3  # Altura da flutuação
    
    def draw(self, surface):
        """Desenha o item"""
        if self.coletado:
            return
            
        # Posição com flutuação
        pos_y = self.rect.y + self.offset_y
        rect_draw = pygame.Rect(self.rect.x, pos_y, self.rect.width, self.rect.height)
        
        # Desenhar item (círculo dourado)
        pygame.draw.circle(surface, self.cor, rect_draw.center, 10)
        pygame.draw.circle(surface, self.cor_borda, rect_draw.center, 10, 2)
        
        # Pequeno brilho no centro
        pygame.draw.circle(surface, (255, 255, 255), rect_draw.center, 4)
    
    def coletar(self):
        """Marca o item como coletado"""
        self.coletado = True
