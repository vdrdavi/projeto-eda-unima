import pygame
from typing import Dict, List, Optional, Tuple
from area_node import AreaNode
from player import Player

class WorldTree:
    def __init__(self, largura_padrao: int = 1920, altura_padrao: int = 1080):
        self.areas: Dict[str, AreaNode] = {}
        self.area_atual: Optional[AreaNode] = None
        self.area_inicial: Optional[AreaNode] = None
        self.largura_padrao = largura_padrao
        self.altura_padrao = altura_padrao
        
        self.criar_mundo()
        
    def criar_area(self, area_id: str, nome: str, cor: Tuple[int, int, int]) -> AreaNode:
        area = AreaNode(area_id, nome, self.largura_padrao, self.altura_padrao)
        area.cor_fundo = cor
        self.areas[area_id] = area
        
        if self.area_inicial is None:
            self.area_inicial = area
            self.area_atual = area
            
        return area
    
    def conectar_areas(self, id_origem: str, id_destino: str, 
                      pos_portal_origem: Tuple[int, int],
                      pos_portal_destino: Tuple[int, int]):
        
        area_origem = self.areas[id_origem]
        area_destino = self.areas[id_destino]
        
        spawn_origem = (pos_portal_destino[0] + 80, pos_portal_destino[1])
        spawn_destino = (pos_portal_origem[0] - 80, pos_portal_origem[1])
        
        area_origem.adicionar_portal(
            pos_portal_origem[0], pos_portal_origem[1], 
            id_destino, spawn_destino[0], spawn_destino[1]
        )
        
        area_destino.adicionar_portal(
            pos_portal_destino[0], pos_portal_destino[1], 
            id_origem, spawn_origem[0], spawn_origem[1]
        )
        
        area_origem.conectar_area(area_destino)
    
    def criar_mundo(self):
        print(" Criando mundo com estrutura de árvore...")
        
        hub = self.criar_area("hub", "Hub Central", (51, 45, 86))
        floresta = self.criar_area("floresta", "Floresta", (34, 87, 46))
        caverna = self.criar_area("caverna", "Caverna", (87, 87, 87))
        deserto = self.criar_area("deserto", "Deserto", (218, 165, 32))
        oceano = self.criar_area("oceano", "Oceano", (25, 25, 112))
        inferno = self.criar_area("inferno", "Inferno", (139, 0, 0))
        
        self._configurar_hub(hub)
        self._configurar_floresta(floresta)
        self._configurar_caverna(caverna)
        self._configurar_deserto(deserto)
        self._configurar_oceano(oceano)
        self._configurar_inferno(inferno)
        
        self.conectar_areas("hub", "floresta", (200, 200), (100, self.altura_padrao - 100))
        self.conectar_areas("hub", "caverna", (self.largura_padrao - 200, 200), (100, 100))
        self.conectar_areas("hub", "deserto", (200, self.altura_padrao - 200), (self.largura_padrao - 100, 100))
        self.conectar_areas("hub", "oceano", (self.largura_padrao - 200, self.altura_padrao - 200), (self.largura_padrao - 100, self.altura_padrao - 100))
        
        self.conectar_areas("caverna", "inferno", (self.largura_padrao - 100, self.altura_padrao // 2), (100, self.altura_padrao // 2))
        
        print(f" Mundo criado com {len(self.areas)} áreas conectadas em árvore")
        
    def _configurar_hub(self, area: AreaNode):
        area.adicionar_parede(0, 0, area.largura, 20)
        area.adicionar_parede(0, area.altura-20, area.largura, 20)
        area.adicionar_parede(0, 0, 20, area.altura)
        area.adicionar_parede(area.largura-20, 0, 20, area.altura)
        
        area.adicionar_parede(400, 300, 200, 20)
        area.adicionar_parede(area.largura-600, area.altura-320, 200, 20)
        
        area.adicionar_item(area.largura//2, area.altura//2)
        area.adicionar_item(300, 400)
        area.adicionar_item(area.largura - 300, 300)
        area.adicionar_item(500, area.altura - 400)
    
    def _configurar_floresta(self, area: AreaNode):
        area.adicionar_parede(0, 0, area.largura, 20)
        area.adicionar_parede(0, area.altura-20, area.largura, 20)
        area.adicionar_parede(0, 0, 20, area.altura)
        area.adicionar_parede(area.largura-20, 0, 20, area.altura)
        
        area.adicionar_parede(300, 200, 80, 80)
        area.adicionar_parede(600, 400, 80, 80)
        area.adicionar_parede(900, 250, 80, 80)
        area.adicionar_parede(400, 600, 80, 80)
        area.adicionar_parede(800, 700, 80, 80)
        
        area.adicionar_item(250, 300)
        area.adicionar_item(550, 500)
        area.adicionar_item(850, 350)
        area.adicionar_item(450, 700)
    
    def _configurar_caverna(self, area: AreaNode):
        area.adicionar_parede(0, 0, area.largura, 20)
        area.adicionar_parede(0, area.altura-20, area.largura, 20)
        area.adicionar_parede(0, 0, 20, area.altura)
        area.adicionar_parede(area.largura-20, 0, 20, area.altura)
        
        area.adicionar_parede(200, 150, 300, 50)
        area.adicionar_parede(600, 300, 50, 200)
        area.adicionar_parede(300, 500, 400, 50)
        area.adicionar_parede(800, 150, 50, 300)
        
        area.adicionar_item(150, 300)
        area.adicionar_item(500, 200)
        area.adicionar_item(700, 450)
        area.adicionar_item(350, 350)
        area.adicionar_item(900, 600)
    
    def _configurar_deserto(self, area: AreaNode):
        area.adicionar_parede(0, 0, area.largura, 20)
        area.adicionar_parede(0, area.altura-20, area.largura, 20)
        area.adicionar_parede(0, 0, 20, area.altura)
        area.adicionar_parede(area.largura-20, 0, 20, area.altura)
        
        area.adicionar_parede(250, 300, 150, 30)
        area.adicionar_parede(500, 200, 200, 30)
        area.adicionar_parede(750, 400, 180, 30)
        area.adicionar_parede(300, 600, 220, 30)
        
        area.adicionar_item(200, 150)
        area.adicionar_item(600, 350)
        area.adicionar_item(850, 250)
        area.adicionar_item(400, 750)
        area.adicionar_item(700, 600)
        area.adicionar_item(100, 500)
    
    def _configurar_oceano(self, area: AreaNode):
        area.adicionar_parede(0, 0, area.largura, 20)
        area.adicionar_parede(0, area.altura-20, area.largura, 20)
        area.adicionar_parede(0, 0, 20, area.altura)
        area.adicionar_parede(area.largura-20, 0, 20, area.altura)
        
        area.adicionar_parede(300, 250, 60, 60)
        area.adicionar_parede(600, 400, 80, 40)
        area.adicionar_parede(450, 600, 70, 70)
        area.adicionar_parede(800, 200, 50, 90)
        area.adicionar_parede(200, 500, 90, 50)
        
        area.adicionar_item(100, 200)
        area.adicionar_item(500, 150)
        area.adicionar_item(750, 350)
        area.adicionar_item(350, 450)
        area.adicionar_item(650, 650)
    
    def _configurar_inferno(self, area: AreaNode):
        area.adicionar_parede(0, 0, area.largura, 20)
        area.adicionar_parede(0, area.altura-20, area.largura, 20)
        area.adicionar_parede(0, 0, 20, area.altura)
        area.adicionar_parede(area.largura-20, 0, 20, area.altura)
        
        area.adicionar_parede(200, 200, 100, 20)
        area.adicionar_parede(400, 350, 20, 100)
        area.adicionar_parede(600, 250, 80, 20)
        area.adicionar_parede(300, 500, 20, 120)
        area.adicionar_parede(700, 450, 100, 20)
        area.adicionar_parede(500, 600, 20, 100)
        
        area.adicionar_item(150, 150)
        area.adicionar_item(450, 200)
        area.adicionar_item(750, 300)
        area.adicionar_item(250, 400)
        area.adicionar_item(550, 500)
        area.adicionar_item(800, 600)
        area.adicionar_item(100, 650)
        area.adicionar_item(650, 150)
    
    def mudar_area(self, novo_area_id: str, player: Player, spawn_x: int = None, spawn_y: int = None):
        if novo_area_id not in self.areas:
            print(f" Área '{novo_area_id}' não existe!")
            return False
            
        nova_area = self.areas[novo_area_id]
        area_anterior = self.area_atual.nome if self.area_atual else "Nenhuma"
        
        self.area_atual = nova_area
        nova_area.marcar_visitada()
        
        if spawn_x is not None and spawn_y is not None:
            player.rect.x = spawn_x
            player.rect.y = spawn_y
        else:
            player.rect.x = nova_area.spawn_x
            player.rect.y = nova_area.spawn_y
            
        print(f" {area_anterior} → {nova_area.nome}")
        return True
    
    def verificar_colisao_portais(self, player: Player) -> Optional[Tuple[str, int, int]]:
        if not self.area_atual:
            return None
            
        for portal in self.area_atual.portais:
            if portal.pode_ser_usado() and player.rect.colliderect(portal.rect):
                return portal.destino_id, portal.spawn_x, portal.spawn_y
                
        return None
    
    def obter_caminho_entre_areas(self, origem_id: str, destino_id: str) -> List[str]:
        if origem_id not in self.areas or destino_id not in self.areas:
            return []
        
        area_origem = self.areas[origem_id]
        area_destino = self.areas[destino_id]
        
        caminho_areas = area_origem.obter_caminho_para(area_destino)
        return [area.area_id for area in caminho_areas]
    
    def obter_areas_adjacentes(self, area_id: str) -> List[str]:
        if area_id not in self.areas:
            return []
        
        area = self.areas[area_id]
        return list(area.conexoes.keys())
    
    def obter_estrutura_arvore(self) -> Dict:
        estrutura = {
            "raiz": "hub",
            "conexoes": {},
            "areas": {}
        }
        
        for area_id, area in self.areas.items():
            estrutura["areas"][area_id] = {
                "nome": area.nome,
                "visitada": area.visitada,
                "conexoes": list(area.conexoes.keys())
            }
            estrutura["conexoes"][area_id] = list(area.conexoes.keys())
        
        return estrutura
    
    def update(self, dt):
        if self.area_atual:
            self.area_atual.update(dt)
    
    def draw(self, surface):
        if self.area_atual:
            surface.fill(self.area_atual.cor_fundo)
            self.area_atual.desenhar(surface)
    
    def obter_estatisticas(self) -> Dict:
        total_areas = len(self.areas)
        areas_visitadas = sum(1 for area in self.areas.values() if area.visitada)
        total_itens = sum(len(area.itens) for area in self.areas.values())
        itens_coletados = sum(1 for area in self.areas.values() for item in area.itens if item.coletado)
        
        return {
            "total_areas": total_areas,
            "areas_visitadas": areas_visitadas,
            "area_atual": self.area_atual.nome if self.area_atual else "Nenhuma",
            "progresso_areas": (areas_visitadas / total_areas * 100) if total_areas > 0 else 0,
            "total_itens": total_itens,
            "itens_coletados": itens_coletados,
            "progresso_itens": (itens_coletados / total_itens * 100) if total_itens > 0 else 0
        }
