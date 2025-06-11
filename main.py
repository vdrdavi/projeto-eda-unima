import pygame
import sys
from player import Player
from world_tree import WorldTree
from inventario import Inventario

FPS = 60

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mouse.set_visible(False)
    
    try:
        som_inicio = pygame.mixer.Sound("sfx/synth.wav")
        som_item = pygame.mixer.Sound("sfx/pickupCoin.wav")
    except pygame.error:
        som_inicio = None
        som_item = None
    
    info = pygame.display.Info()
    LARGURA, ALTURA = info.current_w, info.current_h
    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
    pygame.display.set_caption("Portal Adventure - Tree World")
    relogio = pygame.time.Clock()
    
    if som_inicio:
        som_inicio.play()
    
    mundo = WorldTree(LARGURA, ALTURA)
    jogador = Player(LARGURA//2, ALTURA//2)
    inventario = Inventario()
    itens_coletados = 0
    mostrar_mapa = False
    running = True
    
    while running:
        dt = relogio.tick(FPS) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    running = False
                elif evento.key == pygame.K_i:
                    inventario.toggle_inventario()
                elif evento.key == pygame.K_m:
                    mostrar_mapa = not mostrar_mapa
                elif pygame.K_1 <= evento.key <= pygame.K_9:
                    numero = evento.key - pygame.K_0
                    item_usado = inventario.usar_item(numero)
        
        keys = pygame.key.get_pressed()
        
        if not inventario.aberto and not mostrar_mapa:
            jogador.update(keys, dt)
            jogador.rect.x = max(0, min(jogador.rect.x, LARGURA - jogador.rect.width))
            jogador.rect.y = max(0, min(jogador.rect.y, ALTURA - jogador.rect.height))
            if mundo.area_atual and mundo.area_atual.verificar_colisao_paredes(jogador.rect):
                jogador.update(keys, -dt)
        
        mundo.update(dt)
        
        if mundo.area_atual and not inventario.aberto:
            for item in mundo.area_atual.itens:
                if (not item.coletado and 
                    len(inventario.itens) < 9 and 
                    item.rect.colliderect(jogador.rect)):
                    item.coletar()
                    inventario.adicionar_item("moeda_dourada")
                    itens_coletados += 1
                    if som_item:
                        som_item.play()
        
        if not inventario.aberto:
            resultado_portal = mundo.verificar_colisao_portais(jogador)
            if resultado_portal:
                destino_id, spawn_x, spawn_y = resultado_portal
                mundo.mudar_area(destino_id, jogador, spawn_x, spawn_y)
                corrigir_posicao_jogador(jogador, mundo, LARGURA, ALTURA)
        
        mundo.draw(tela)
        jogador.draw(tela)
        desenhar_interface(tela, mundo, inventario, itens_coletados, mostrar_mapa)
        inventario.desenhar(tela)
        pygame.display.flip()
    
    pygame.mouse.set_visible(True)
    pygame.quit()
    sys.exit()

def corrigir_posicao_jogador(jogador, mundo, largura, altura):
    if not mundo.area_atual:
        return
    if not mundo.area_atual.verificar_colisao_paredes(jogador.rect):
        return
    posicao_original = (jogador.rect.x, jogador.rect.y)
    for raio in range(50, 300, 25):
        for angulo in range(0, 360, 30):
            import math
            rad = math.radians(angulo)
            novo_x = int(posicao_original[0] + raio * math.cos(rad))
            novo_y = int(posicao_original[1] + raio * math.sin(rad))
            novo_x = max(0, min(novo_x, largura - jogador.rect.width))
            novo_y = max(0, min(novo_y, altura - jogador.rect.height))
            teste_rect = pygame.Rect(novo_x, novo_y, jogador.rect.width, jogador.rect.height)
            if not mundo.area_atual.verificar_colisao_paredes(teste_rect):
                jogador.rect.x = novo_x
                jogador.rect.y = novo_y
                return
    jogador.rect.x = largura // 2
    jogador.rect.y = altura // 2
    if mundo.area_atual.verificar_colisao_paredes(jogador.rect):
        for offset_x in range(-100, 101, 25):
            for offset_y in range(-100, 101, 25):
                teste_x = (largura // 2) + offset_x
                teste_y = (altura // 2) + offset_y
                teste_x = max(0, min(teste_x, largura - jogador.rect.width))
                teste_y = max(0, min(teste_y, altura - jogador.rect.height))
                teste_rect = pygame.Rect(teste_x, teste_y, jogador.rect.width, jogador.rect.height)
                if not mundo.area_atual.verificar_colisao_paredes(teste_rect):
                    jogador.rect.x = teste_x
                    jogador.rect.y = teste_y
                    return

def desenhar_interface(tela, mundo, inventario, itens_coletados, mostrar_mapa):
    LARGURA, ALTURA = tela.get_size()
    if mundo.area_atual:
        font = pygame.font.Font(None, 48)
        texto_area = font.render(mundo.area_atual.nome, True, (255, 255, 255))
        tela.blit(texto_area, (LARGURA//2 - texto_area.get_width()//2, 30))
    font_contador = pygame.font.Font(None, 36)
    texto_contador = font_contador.render(f"Itens coletados: {itens_coletados}", True, (255, 255, 255))
    tela.blit(texto_contador, (20, 20))
    font_status = pygame.font.Font(None, 24)
    status_inventario = f"Inventário: {len(inventario.itens)}/9"
    cor_status = (255, 255, 0) if len(inventario.itens) < 9 else (255, 100, 100)
    texto_status = font_status.render(status_inventario, True, cor_status)
    tela.blit(texto_status, (20, 60))
    if mostrar_mapa:
        desenhar_mapa_estrutura(tela, mundo)

def desenhar_mapa_estrutura(tela, mundo):
    LARGURA, ALTURA = tela.get_size()
    mapa_rect = pygame.Rect(LARGURA//4, ALTURA//4, LARGURA//2, ALTURA//2)
    pygame.draw.rect(tela, (0, 0, 0, 180), mapa_rect)
    pygame.draw.rect(tela, (255, 255, 255), mapa_rect, 3)
    font_titulo = pygame.font.Font(None, 36)
    titulo = font_titulo.render("ESTRUTURA DO MUNDO", True, (255, 255, 255))
    titulo_rect = titulo.get_rect(center=(LARGURA//2, mapa_rect.y + 30))
    tela.blit(titulo, titulo_rect)
    font_area = pygame.font.Font(None, 24)
    y_offset = mapa_rect.y + 70
    hub = mundo.areas.get("hub")
    if hub:
        cor = (255, 255, 0) if hub == mundo.area_atual else (0, 255, 0) if hub.visitada else (255, 255, 255)
        prefixo = "🏛️ " if hub == mundo.area_atual else "✓ " if hub.visitada else "○ "
        texto = font_area.render(f"{prefixo}HUB: {hub.nome}", True, cor)
        tela.blit(texto, (mapa_rect.x + 20, y_offset))
        y_offset += 35
        for area_id in hub.conexoes.keys():
            if area_id != "caverna":
                area = mundo.areas[area_id]
                cor = (255, 255, 0) if area == mundo.area_atual else (0, 255, 0) if area.visitada else (255, 255, 255)
                prefixo = "  ├─ ➤ " if area == mundo.area_atual else "  ├─ ✓ " if area.visitada else "  ├─ ○ "
                texto = font_area.render(f"{prefixo}{area.nome}", True, cor)
                tela.blit(texto, (mapa_rect.x + 20, y_offset))
                y_offset += 25
        caverna = mundo.areas.get("caverna")
        if caverna:
            cor = (255, 255, 0) if caverna == mundo.area_atual else (0, 255, 0) if caverna.visitada else (255, 255, 255)
            prefixo = "  └─ ➤ " if caverna == mundo.area_atual else "  └─ ✓ " if caverna.visitada else "  └─ ○ "
            texto = font_area.render(f"{prefixo}{caverna.nome}", True, cor)
            tela.blit(texto, (mapa_rect.x + 20, y_offset))
            y_offset += 25
            inferno = mundo.areas.get("inferno")
            if inferno and "inferno" in caverna.conexoes:
                cor = (255, 255, 0) if inferno == mundo.area_atual else (0, 255, 0) if inferno.visitada else (255, 255, 255)
                prefixo = "     └─ ➤ " if inferno == mundo.area_atual else "     └─ ✓ " if inferno.visitada else "     └─ ○ "
                texto = font_area.render(f"{prefixo}{inferno.nome}", True, cor)
                tela.blit(texto, (mapa_rect.x + 20, y_offset))
                y_offset += 25
    estatisticas = mundo.obter_estatisticas()
    font_stats = pygame.font.Font(None, 20)
    stats_text = [
        f"Progresso: {estatisticas['progresso_areas']:.1f}%",
        f"Áreas: {estatisticas['areas_visitadas']}/{estatisticas['total_areas']}",
        f"Itens: {estatisticas['itens_coletados']}/{estatisticas['total_itens']}"
    ]
    y_stats = mapa_rect.bottom - 80
    for linha in stats_text:
        texto_stat = font_stats.render(linha, True, (200, 200, 200))
        tela.blit(texto_stat, (mapa_rect.x + 20, y_stats))
        y_stats += 25

if __name__ == "__main__":
    main()

