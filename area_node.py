import pygame
from typing import List, Dict, Optional, Tuple
from parede import Parede
from item import Item
from portal import Portal
class AreaNode:
    def __init__(self, area_id: str, nome: str, largura: int, altura: int):
        self.area_id = area_id
        self.nome = nome
        self.largura = largura
        self.altura = altura
        
        # Elementos da área
        self.paredes: List[Parede] = []
        self.itens: List[Item] = []
        self.portais: List[Portal] = []
        
        # Conexões com outras áreas
        self.conexoes: Dict[str, 'AreaNode'] = {}
        self.area_pai: Optional['AreaNode'] = None
        self.areas_filhas: List['AreaNode'] = []
        
        # Posição de spawn do jogador
        self.spawn_x = largura // 2
        self.spawn_y = altura // 2
        
        # Metadados
        self.visitada = False
        self.desbloqueada = True  # Por padrão, área está desbloqueada
        self.nivel_profundidade = 0
        
    def adicionar_parede(self, x: int, y: int, width: int, height: int):
        """Adiciona uma parede à área"""
        parede = Parede(x, y, width, height)
        self.paredes.append(parede)
        return parede
    
    def adicionar_item(self, x: int, y: int):
        """Adiciona um item à área"""
        item = Item(x, y)
        self.itens.append(item)
        return item
    
    def adicionar_portal(self, x: int, y: int, destino_id: str, spawn_x: int = None, spawn_y: int = None):
        """Adiciona um portal para outra área"""
        portal = Portal(x, y, destino_id, spawn_x, spawn_y)
        self.portais.append(portal)
        return portal
    
    def conectar_area(self, area_destino: 'AreaNode', bidirecional: bool = True):
        """Conecta esta área com outra área"""
        self.conexoes[area_destino.area_id] = area_destino
        if bidirecional:
            area_destino.conexoes[self.area_id] = self
    
    def adicionar_area_filha(self, area_filha: 'AreaNode'):
        """Adiciona uma área filha na estrutura de árvore"""
        if area_filha not in self.areas_filhas:
            self.areas_filhas.append(area_filha)
            area_filha.area_pai = self
            area_filha.nivel_profundidade = self.nivel_profundidade + 1
            self.conectar_area(area_filha)
    
    def esta_acessivel_de(self, area_origem: 'AreaNode') -> bool:
        """Verifica se esta área é acessível a partir de outra área"""
        if not self.desbloqueada:
            return False
        
        # BFS para encontrar caminho
        visitadas = set()
        fila = [area_origem]
        
        while fila:
            area_atual = fila.pop(0)
            if area_atual.area_id in visitadas:
                continue
                
            visitadas.add(area_atual.area_id)
            
            if area_atual.area_id == self.area_id:
                return True
                
            for area_conectada in area_atual.conexoes.values():
                if area_conectada.desbloqueada and area_conectada.area_id not in visitadas:
                    fila.append(area_conectada)
        
        return False
    
    def obter_caminho_para(self, area_destino: 'AreaNode') -> List['AreaNode']:
        """Retorna o caminho mais curto para outra área"""
        if not area_destino.desbloqueada:
            return []
        
        # BFS para encontrar o caminho mais curto
        visitadas = set()
        fila = [(self, [self])]
        
        while fila:
            area_atual, caminho = fila.pop(0)
            
            if area_atual.area_id in visitadas:
                continue
                
            visitadas.add(area_atual.area_id)
            
            if area_atual.area_id == area_destino.area_id:
                return caminho
                
            for area_conectada in area_atual.conexoes.values():
                if area_conectada.desbloqueada and area_conectada.area_id not in visitadas:
                    novo_caminho = caminho + [area_conectada]
                    fila.append((area_conectada, novo_caminho))
        
        return []
    
    def definir_spawn(self, x: int, y: int):
        """Define a posição de spawn do jogador nesta área"""
        self.spawn_x = x
        self.spawn_y = y
    
    def marcar_visitada(self):
        """Marca a área como visitada"""
        self.visitada = True
    
    def desbloquear(self):
        """Desbloqueia a área"""
        self.desbloqueada = True
    
    def bloquear(self):
        """Bloqueia a área"""
        self.desbloqueada = False
    
    def desenhar(self, surface):
        """Desenha todos os elementos da área"""
        # Desenhar paredes
        for parede in self.paredes:
            parede.draw(surface)
        
        # Desenhar itens
        for item in self.itens:
            item.draw(surface)
            
        # Desenhar portais
        for portal in self.portais:
            portal.draw(surface)
    
    def __str__(self):
        return f"Área {self.area_id}: {self.nome} (Nível {self.nivel_profundidade})"
    
    def __repr__(self):
        return self.__str__()
