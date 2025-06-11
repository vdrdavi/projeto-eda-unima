import pygame
from typing import List, Dict
from parede import Parede
from item import Item
from portal import Portal

class AreaNode:
    def __init__(self, area_id: str, nome: str, largura: int, altura: int):
        self.area_id = area_id
        self.nome = nome
        self.largura = largura
        self.altura = altura
        self.paredes: List[Parede] = []
        self.itens: List[Item] = []
        self.portais: List[Portal] = []
        self.conexoes: Dict[str, 'AreaNode'] = {}
        self.spawn_x = largura // 2
        self.spawn_y = altura // 2
        self.visitada = False
        self.cor_fundo = (100, 100, 100)
        
    def adicionar_parede(self, x: int, y: int, width: int, height: int):
        parede = Parede(x, y, width, height)
        self.paredes.append(parede)
        return parede
    
    def adicionar_item(self, x: int, y: int):
        item = Item(x, y)
        self.itens.append(item)
        return item
    
    def adicionar_portal(self, x: int, y: int, destino_id: str, spawn_x: int, spawn_y: int):
        portal = Portal(x, y, destino_id, spawn_x, spawn_y)
        self.portais.append(portal)
        print(f" Portal criado: {self.area_id} → {destino_id} em ({x}, {y})")
        return portal
    
    def conectar_area(self, area_destino: 'AreaNode'):
        self.conexoes[area_destino.area_id] = area_destino
        area_destino.conexoes[self.area_id] = self
    
    def obter_caminho_para(self, area_destino: 'AreaNode') -> List['AreaNode']:
        if self.area_id == area_destino.area_id:
            return [self]
        
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
                if area_conectada.area_id not in visitadas:
                    novo_caminho = caminho + [area_conectada]
                    fila.append((area_conectada, novo_caminho))
        
        return []
    
    def verificar_colisao_paredes(self, rect: pygame.Rect) -> bool:
        for parede in self.paredes:
            if rect.colliderect(parede.rect):
                return True
        return False
    
    def marcar_visitada(self):
        if not self.visitada:
            self.visitada = True
            print(f"🗺️  Primeira visita: {self.nome}")
    
    def desenhar(self, surface):
        for parede in self.paredes:
            parede.draw(surface)
        for item in self.itens:
            item.draw(surface)
        for portal in self.portais:
            portal.draw(surface)
    
    def update(self, dt):
        for item in self.itens:
            item.update(dt)
        for portal in self.portais:
            portal.update(dt)
    
    def __str__(self):
        visitado = "" if self.visitada else ""
        return f"{self.nome} {visitado}"
    
    def __repr__(self):
        return f"AreaNode({self.area_id}, {self.nome})"

