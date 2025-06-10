import pygame
from typing import Dict, List, Optional, Tuple
from area_node import AreaNode
from player import Player
import random

class WorldTree:
    def __init__(self, largura_padrao: int = 1920, altura_padrao: int = 1080):
        self.areas: Dict[str, AreaNode] = {}
        self.area_atual: Optional[AreaNode] = None
        self.area_inicial: Optional[AreaNode] = None
        self.largura_padrao = largura_padrao
        self.altura_padrao = altura_padrao
        
        # Configurações de geração
        self.max_profundidade = 5
        self.max_areas_por_nivel = 3
        
    def criar_area(self, area_id: str, nome: str, largura: int = None, altura: int = None) -> AreaNode:
        """Cria uma nova área"""
        largura = largura or self.largura_padrao
        altura = altura or self.altura_padrao
        
        area = AreaNode(area_id, nome, largura, altura)
        self.areas[area_id] = area
        
        if self.area_inicial is None:
            self.area_inicial = area
            self.area_atual = area
            
        return area
    
    def conectar_areas(self, id_origem: str, id_destino: str, 
                      pos_portal_origem: Tuple[int, int],
                      pos_portal_destino: Tuple[int, int],
                      pos_spawn_origem: Tuple[int, int],
                      pos_spawn_destino: Tuple[int, int]):
        """Conecta duas áreas com portais bidirecionais"""
        
        area_origem = self.areas.get(id_origem)
        area_destino = self.areas.get(id_destino)
        
        if not area_origem or not area_destino:
            raise ValueError("Uma das áreas não existe")
        
        # Posições padrão se não especificadas
        if pos_portal_origem is None:
            pos_portal_origem = (area_origem.largura - 80, area_origem.altura // 2)
        if pos_portal_destino is None:
            pos_portal_destino = (40, area_destino.altura // 2)
        if pos_spawn_origem is None:
            pos_spawn_origem = (pos_portal_destino[0] + 80, pos_portal_destino[1])
        if pos_spawn_destino is None:
            pos_spawn_destino = (pos_portal_origem[0] - 80, pos_portal_origem[1])
        
        # Criar portais
        area_origem.adicionar_portal(
            pos_portal_origem[0], pos_portal_origem[1], 
            id_destino, pos_spawn_destino[0], pos_spawn_destino[1]
        )
        
        area_destino.adicionar_portal(
            pos_portal_destino[0], pos_portal_destino[1], 
            id_origem, pos_spawn_origem[0], pos_spawn_origem[1]
        )
        
        # Conectar áreas
        area_origem.conectar_area(area_destino)
    
    def mudar_area(self, novo_area_id: str, player: Player, spawn_x: int = None, spawn_y: int = None):
        """Muda o jogador para uma nova área"""
        if novo_area_id not in self.areas:
            return False
            
        nova_area = self.areas[novo_area_id]
        
        if not nova_area.desbloqueada:
            return False
            
        self.area_atual = nova_area
        nova_area.marcar_visitada()
        
        # Posicionar jogador
        if spawn_x is not None and spawn_y is not None:
            player.rect.x = spawn_x
            player.rect.y = spawn_y
        else:
            player.rect.x = nova_area.spawn_x
            player.rect.y = nova_area.spawn_y
            
        return True
    
    def verificar_colisao_portais(self, player: Player) -> Optional[str]:
        """Verifica se o jogador colidiu com algum portal"""
        if not self.area_atual:
            return None
            
        for portal in self.area_atual.portais:
            if portal.pode_ser_usado() and player.rect.colliderect(portal.rect):
                return portal.destino_id
                
        return None
    
    def obter_spawn_portal(self, area_id: str, origem_id: str) -> Tuple[int, int]:
        """Obtém a posição de spawn ao usar um portal"""
        area = self.areas.get(area_id)
        if not area:
            return area.spawn_x, area.spawn_y
            
        # Procurar portal que vem da área de origem
        for portal in area.portais:
            if portal.destino_id == origem_id:
                return portal.spawn_x, portal.spawn_y
                
        return area.spawn_x, area.spawn_y
    
    def gerar_mundo_procedural(self, area_raiz_id: str = "hub"):
        """Gera um mundo procedural em forma de árvore"""
        # Criar área central (hub)
        hub = self.criar_area(area_raiz_id, "Hub Central")
        self._criar_paredes_basicas(hub)
        
        # Gerar áreas em níveis
        areas_atuais = [hub]
        
        for nivel in range(1, self.max_profundidade + 1):
            novas_areas = []
            
            for area_pai in areas_atuais:
                num_filhas = random.randint(1, self.max_areas_por_nivel)
                
                for i in range(num_filhas):
                    area_id = f"area_{nivel}_{len(novas_areas)}"
                    nome = f"Área {nivel}-{i+1}"
                    
                    nova_area = self.criar_area(area_id, nome)
                    self._criar_layout_aleatorio(nova_area, nivel)
                    
                    area_pai.adicionar_area_filha(nova_area)
                    novas_areas.append(nova_area)
                    
                    # Conectar com portal
                    self.conectar_areas(area_pai.area_id, nova_area.area_id)
            
            areas_atuais = novas_areas
            
            # Parar se não há mais áreas para expandir
            if not novas_areas:
                break
    
    def _criar_paredes_basicas(self, area: AreaNode):
        """Cria paredes básicas para uma área"""
        # Bordas
        area.adicionar_parede(0, 0, area.largura, 20)  # Superior
        area.adicionar_parede(0, area.altura-20, area.largura, 20)  # Inferior
        area.adicionar_parede(0, 0, 20, area.altura)  # Esquerda
        area.adicionar_parede(area.largura-20, 0, 20, area.altura)  # Direita
    
    def _criar_layout_aleatorio(self, area: AreaNode, nivel: int):
        """Cria um layout aleatório para uma área"""
        self._criar_paredes_basicas(area)
        
        # Adicionar algumas paredes internas aleatórias
        num_paredes = random.randint(2, 5)
        for _ in range(num_paredes):
            x = random.randint(100, area.largura - 200)
            y = random.randint(100, area.altura - 200)
            
            if random.choice([True, False]):
                # Parede horizontal
                area.adicionar_parede(x, y, random.randint(50, 150), 20)
            else:
                # Parede vertical
                area.adicionar_parede(x, y, 20, random.randint(50, 150))
        
        # Adicionar itens baseado no nível
        num_itens = random.randint(nivel, nivel * 2)
        for _ in range(num_itens):
            x = random.randint(50, area.largura - 50)
            y = random.randint(50, area.altura - 50)
            area.adicionar_item(x, y)
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas do mundo"""
        total_areas = len(self.areas)
        areas_visitadas = sum(1 for area in self.areas.values() if area.visitada)
        areas_desbloqueadas = sum(1 for area in self.areas.values() if area.desbloqueada)
        
        return {
            "total_areas": total_areas,
            "areas_visitadas": areas_visitadas,
            "areas_desbloqueadas": areas_desbloqueadas,
            "area_atual": self.area_atual.nome if self.area_atual else "Nenhuma",
            "progresso": (areas_visitadas / total_areas * 100) if total_areas > 0 else 0
        }
    
    def validar_acessibilidade(self) -> List[str]:
        """Valida se todas as áreas são acessíveis a partir da área inicial"""
        problemas = []
        
        if not self.area_inicial:
            problemas.append("Nenhuma área inicial definida")
            return problemas
        
        for area_id, area in self.areas.items():
            if not area.esta_acessivel_de(self.area_inicial):
                problemas.append(f"Área '{area.nome}' ({area_id}) não é acessível")
        
        return problemas
    
    def update(self, dt):
        """Atualiza elementos da área atual"""
        if self.area_atual:
            for portal in self.area_atual.portais:
                portal.update(dt)
    
    def draw(self, surface):
        """Desenha a área atual"""
        if self.area_atual:
            self.area_atual.desenhar(surface)
