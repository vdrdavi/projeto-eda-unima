import pygame
import sys
import random
from player import Player
from portal import Portal
from item import Item
from inventario import Inventario

# Configurações
FPS = 60

# Definir áreas com cores diferentes
AREAS = {
    "hub": (51, 45, 86),          # Roxo escuro - área inicial
    "floresta": (34, 87, 46),     # Verde floresta
    "caverna": (87, 87, 87),      # Cinza caverna
    "deserto": (218, 165, 32),    # Dourado deserto
    "oceano": (25, 25, 112),      # Azul oceano
    "inferno": (139, 0, 0),       # Vermelho inferno
}

def gerar_itens_aleatorios(largura, altura, quantidade=6):
    """Gera itens em posições aleatórias, evitando as bordas"""
    itens = []
    for _ in range(quantidade):
        x = random.randint(100, largura - 120)  # Evitar bordas
        y = random.randint(100, altura - 120)
        itens.append(Item(x, y))
    return itens

def main():
    # Inicializar Pygame
    pygame.init()
    pygame.mixer.init()  # Inicializar mixer para sons
    
    # Esconder cursor
    pygame.mouse.set_visible(False)
    
    # Carregar sons
    try:
        som_inicio = pygame.mixer.Sound("sfx/synth.wav")
        som_item = pygame.mixer.Sound("sfx/pickupCoin.wav")
        print("Sons carregados com sucesso!")
    except pygame.error as e:
        print(f"Erro ao carregar sons: {e}")
        som_inicio = None
        som_item = None
    
    # Obter dimensões da tela para fullscreen
    info = pygame.display.Info()
    LARGURA, ALTURA = info.current_w, info.current_h
    
    # Criar tela em fullscreen
    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
    pygame.display.set_caption("Portal Adventure")
    relogio = pygame.time.Clock()
    
    # Tocar som de início
    if som_inicio:
        som_inicio.play()
    
    # Área atual
    area_atual = "hub"
    
    # Contador de itens coletados
    itens_coletados = 0
    
    # Criar player no centro da tela
    jogador = Player(LARGURA//2, ALTURA//2)
    
    # Criar inventário
    inventario = Inventario()
    
    # Criar portais para diferentes áreas (no hub)
    portais_hub = [
        Portal(100, 100, "floresta", LARGURA//2, ALTURA//2),
        Portal(LARGURA-140, 100, "caverna", LARGURA//2, ALTURA//2),
        Portal(100, ALTURA-160, "deserto", LARGURA//2, ALTURA//2),
        Portal(LARGURA-140, ALTURA-160, "oceano", LARGURA//2, ALTURA//2),
        Portal(LARGURA//2-20, 100, "inferno", LARGURA//2, ALTURA//2),
    ]
    
    # Portais de volta para o hub
    portais_volta = {
        "floresta": Portal(LARGURA//2-20, ALTURA-160, "hub", LARGURA//2, ALTURA//2),
        "caverna": Portal(LARGURA//2-20, ALTURA-160, "hub", LARGURA//2, ALTURA//2),
        "deserto": Portal(LARGURA//2-20, ALTURA-160, "hub", LARGURA//2, ALTURA//2),
        "oceano": Portal(LARGURA//2-20, ALTURA-160, "hub", LARGURA//2, ALTURA//2),
        "inferno": Portal(LARGURA//2-20, ALTURA-160, "hub", LARGURA//2, ALTURA//2),
    }
    
    # Gerar itens para cada área
    itens_por_area = {}
    for area in AREAS.keys():
        itens_por_area[area] = gerar_itens_aleatorios(LARGURA, ALTURA, 6)
    
    running = True
    while running:
        dt = relogio.tick(FPS) / 1000.0
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    running = False
                elif evento.key == pygame.K_i:  # Abrir/fechar inventário
                    inventario.toggle_inventario()
                    print("Inventário", "aberto" if inventario.aberto else "fechado")
                elif pygame.K_1 <= evento.key <= pygame.K_9:  # Usar itens (1-9)
                    numero = evento.key - pygame.K_0
                    item_usado = inventario.usar_item(numero)
                    if item_usado:
                        print(f"Item {item_usado} usado do slot {numero}!")
        
        # Capturar teclas pressionadas
        keys = pygame.key.get_pressed()
        
        # **NOVO: Só atualizar player se inventário estiver fechado**
        if not inventario.aberto:
            # Atualizar player
            jogador.update(keys, dt)
            
            # Manter player dentro da tela
            jogador.rect.x = max(0, min(jogador.rect.x, LARGURA - jogador.rect.width))
            jogador.rect.y = max(0, min(jogador.rect.y, ALTURA - jogador.rect.height))
        
        # Atualizar itens da área atual
        itens_atuais = itens_por_area[area_atual]
        for item in itens_atuais:
            if not item.coletado:
                item.update(dt)
                # **NOVO: Só coletar se inventário não estiver cheio e fechado**
                if (not inventario.aberto and 
                    len(inventario.itens) < 9 and  # Inventário não está cheio
                    item.rect.colliderect(jogador.rect)):
                    
                    item.coletar()
                    inventario.adicionar_item("moeda_dourada")  # Adicionar ao inventário
                    itens_coletados += 1
                    if som_item:
                        som_item.play()
                    print(f"Item coletado! Total: {itens_coletados}")
                
                # **NOVO: Feedback quando inventário está cheio**
                elif (not inventario.aberto and 
                      len(inventario.itens) >= 9 and 
                      item.rect.colliderect(jogador.rect)):
                    print("Inventário cheio! Não é possível coletar mais itens.")
        
        # **NOVO: Só verificar portais se inventário estiver fechado**
        if not inventario.aberto:
            # Verificar colisão com portais e transportar
            if area_atual == "hub":
                for portal in portais_hub:
                    portal.update(dt)
                    if portal.pode_ser_usado() and portal.rect.colliderect(jogador.rect):
                        area_atual = portal.destino_id
                        jogador.rect.x = portal.spawn_x
                        jogador.rect.y = portal.spawn_y
                        print(f"Transportado para: {area_atual}")
            else:
                portal_volta = portais_volta[area_atual]
                portal_volta.update(dt)
                if portal_volta.pode_ser_usado() and portal_volta.rect.colliderect(jogador.rect):
                    area_atual = portal_volta.destino_id
                    jogador.rect.x = portal_volta.spawn_x
                    jogador.rect.y = portal_volta.spawn_y
                    print(f"Voltou para: {area_atual}")
        else:
            # Atualizar portais mesmo com inventário aberto (para animação)
            if area_atual == "hub":
                for portal in portais_hub:
                    portal.update(dt)
            else:
                portais_volta[area_atual].update(dt)
        
        # Desenhar
        cor_fundo_atual = AREAS[area_atual]
        tela.fill(cor_fundo_atual)
        
        # Desenhar itens da área atual
        for item in itens_atuais:
            item.draw(tela)
        
        # Desenhar portais
        if area_atual == "hub":
            for portal in portais_hub:
                portal.draw(tela)
                
            # Texto informativo
            font = pygame.font.Font(None, 48)
            texto = font.render("HUB - Colete os itens dourados!", True, (255, 255, 255))
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 30))
            
            # Labels dos portais
            font_pequena = pygame.font.Font(None, 24)
            labels = ["Floresta", "Caverna", "Deserto", "Oceano", "Inferno"]
            posicoes_labels = [
                (100, 70), (LARGURA-140, 70), (100, ALTURA-180), 
                (LARGURA-140, ALTURA-180), (LARGURA//2-20, 70)
            ]
            
            for i, (label, pos) in enumerate(zip(labels, posicoes_labels)):
                texto_label = font_pequena.render(label, True, (255, 255, 255))
                tela.blit(texto_label, (pos[0], pos[1]))
                
        else:
            portais_volta[area_atual].draw(tela)
            
            # Texto da área atual
            font = pygame.font.Font(None, 48)
            nome_area = area_atual.capitalize()
            texto = font.render(f"Área: {nome_area}", True, (255, 255, 255))
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 30))
        
        # Mostrar contador de itens coletados
        font_contador = pygame.font.Font(None, 36)
        texto_contador = font_contador.render(f"Itens coletados: {itens_coletados}", True, (255, 255, 255))
        tela.blit(texto_contador, (20, 20))
        
        # **NOVO: Mostrar status do inventário**
        font_status = pygame.font.Font(None, 24)
        status_inventario = f"Inventário: {len(inventario.itens)}/9"
        cor_status = (255, 255, 0) if len(inventario.itens) < 9 else (255, 100, 100)  # Amarelo ou vermelho se cheio
        texto_status = font_status.render(status_inventario, True, cor_status)
        tela.blit(texto_status, (20, 60))
        
        # Mostrar instruções
        if len(inventario.itens) > 0:
            font_instrucao = pygame.font.Font(None, 24)
            texto_instrucao = font_instrucao.render("Pressione I para abrir inventário", True, (255, 255, 0))
            tela.blit(texto_instrucao, (20, 85))
            
        # **NOVO: Aviso de inventário cheio**
        if len(inventario.itens) >= 9:
            font_aviso = pygame.font.Font(None, 28)
            texto_aviso = font_aviso.render("INVENTÁRIO CHEIO! Use itens (1-9) para liberar espaço", True, (255, 50, 50))
            tela.blit(texto_aviso, (LARGURA//2 - texto_aviso.get_width()//2, ALTURA - 50))
        
        # Desenhar player
        jogador.draw(tela)
        
        # Desenhar inventário (deve ser por último para ficar por cima)
        inventario.desenhar(tela)
        
        pygame.display.flip()
    
    # Mostrar mouse antes de sair
    pygame.mouse.set_visible(True)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
