import pygame

class Portal:
    def __init__(self, x: int, y: int, destino_id: str, spawn_x: int = None, spawn_y: int = None):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.destino_id = destino_id
        self.spawn_x = spawn_x or x
        self.spawn_y = spawn_y or y
        
        # Visual do portal
        self.color = (138, 43, 226)  # Roxo
        self.borda_color = (75, 0, 130)  # Roxo mais escuro
        self.ativo = True
        
        # Animação
        self.animacao_offset = 0
        self.velocidade_animacao = 2
    
    def update(self, dt):
        """Atualiza a animação do portal"""
        if self.ativo:
            self.animacao_offset += self.velocidade_animacao * dt
            if self.animacao_offset > 2 * 3.14159:  # 2π para completar o ciclo
                self.animacao_offset = 0
    
    def draw(self, surface):
        """Desenha o portal"""
        if not self.ativo:
            return
            
        # Efeito de brilho animado
        import math
        intensidade = int(50 + 30 * math.sin(self.animacao_offset))
        color_animada = (
            min(255, self.color[0] + intensidade),
            min(255, self.color[1] + intensidade//2),
            min(255, self.color[2] + intensidade)
        )
        
        # Desenhar portal
        pygame.draw.ellipse(surface, color_animada, self.rect)
        pygame.draw.ellipse(surface, self.borda_color, self.rect, 3)
        
        # Desenhar centro mais claro
        centro_rect = pygame.Rect(
            self.rect.x + 10, self.rect.y + 15,
            self.rect.width - 20, self.rect.height - 30
        )
        pygame.draw.ellipse(surface, (200, 150, 255), centro_rect)
    
    def pode_ser_usado(self) -> bool:
        """Verifica se o portal pode ser usado"""
        return self.ativo
    
    def ativar(self):
        """Ativa o portal"""
        self.ativo = True
    
    def desativar(self):
        """Desativa o portal"""
        self.ativo = False
