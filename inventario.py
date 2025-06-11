import pygame

class Inventario:
    def __init__(self, max_slots=9):
        self.itens = []
        self.max_slots = max_slots
        self.aberto = False
        self.slots_por_linha = 3
        self.tamanho_slot = 60
        self.espacamento = 10
        self.font = pygame.font.Font(None, 24)
        
    def adicionar_item(self, tipo_item="coletavel"):
        if len(self.itens) < self.max_slots:
            self.itens.append(tipo_item)
            return True
        return False
    
    def remover_item(self, indice):
        if 0 <= indice < len(self.itens):
            return self.itens.pop(indice)
        return None
    
    def toggle_inventario(self):
        self.aberto = not self.aberto
    
    def desenhar(self, surface):
        if not self.aberto:
            return
            
        largura_tela, altura_tela = surface.get_size()
        largura_inventario = (self.slots_por_linha * self.tamanho_slot) + ((self.slots_por_linha + 1) * self.espacamento)
        linhas = (self.max_slots + self.slots_por_linha - 1) // self.slots_por_linha
        altura_inventario = (linhas * self.tamanho_slot) + ((linhas + 1) * self.espacamento) + 60
        x_inventario = (largura_tela - largura_inventario) // 2
        y_inventario = (altura_tela - altura_inventario) // 2
        
        fundo_rect = pygame.Rect(x_inventario, y_inventario, largura_inventario, altura_inventario)
        pygame.draw.rect(surface, (50, 50, 50), fundo_rect)
        pygame.draw.rect(surface, (200, 200, 200), fundo_rect, 3)
        
        titulo = self.font.render("INVENTÁRIO", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(x_inventario + largura_inventario//2, y_inventario + 25))
        surface.blit(titulo, titulo_rect)
        
        for i in range(self.max_slots):
            linha = i // self.slots_por_linha
            coluna = i % self.slots_por_linha
            slot_x = x_inventario + self.espacamento + (coluna * (self.tamanho_slot + self.espacamento))
            slot_y = y_inventario + 50 + self.espacamento + (linha * (self.tamanho_slot + self.espacamento))
            slot_rect = pygame.Rect(slot_x, slot_y, self.tamanho_slot, self.tamanho_slot)
            
            if i < len(self.itens):
                pygame.draw.rect(surface, (100, 100, 100), slot_rect)
                pygame.draw.rect(surface, (255, 215, 0), slot_rect, 2)
                centro_x = slot_x + self.tamanho_slot // 2
                centro_y = slot_y + self.tamanho_slot // 2
                pygame.draw.circle(surface, (255, 215, 0), (centro_x, centro_y), 15)
                numero = self.font.render(str(i + 1), True, (0, 0, 0))
                numero_rect = numero.get_rect(center=(centro_x, centro_y))
                surface.blit(numero, numero_rect)
            else:
                pygame.draw.rect(surface, (80, 80, 80), slot_rect)
                pygame.draw.rect(surface, (120, 120, 120), slot_rect, 2)
        
        if len(self.itens) > 0:
            instrucao = "Pressione 1-9 para usar item"
            instrucao_surface = pygame.font.Font(None, 20).render(instrucao, True, (255, 215, 0))
            instrucao_rect = instrucao_surface.get_rect(center=(largura_tela//2, y_inventario - 20))
            surface.blit(instrucao_surface, instrucao_rect)
    
    def usar_item(self, numero_slot):
        indice = numero_slot - 1
        if 0 <= indice < len(self.itens):
            item_usado = self.remover_item(indice)
            return item_usado
        return None
    
    def esta_cheio(self):
        return len(self.itens) >= self.max_slots
    
    def esta_vazio(self):
        return len(self.itens) == 0

