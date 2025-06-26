import pygame

# Cores
VERDE = (34, 139, 34)
LEGENDA = (0, 153, 18)
AZUL = (9, 0, 133)
CINZA = (169, 169, 169)
AMARELO = (255, 215, 0)
PRETO = (0, 0, 0)

def desenhar_planta(tela, planta, fonte):
    # Define cor com base no status
    if planta.morta:
        cor = (100, 100, 100)  # Cinza escuro
    elif planta.coletada:
        cor = CINZA
    else:
        cor = VERDE

    tamanho = int(10 + planta.maturidade / 10)
    
    # Corpo da planta
    pygame.draw.circle(tela, cor, (planta.x, planta.y), tamanho)

    # Barra de água
    pygame.draw.rect(tela, AZUL, (planta.x - 10, planta.y + 10, planta.agua / 5, 5))

    # Texto de status
    status = f"M: {int(planta.maturidade)}%  A: {int(planta.agua)}"
    if planta.morta:
        status += "  Morta"
    elif planta.coletada:
        status += "  Coletada"
    
    texto_status = fonte.render(status, True, PRETO)
    texto_pos = texto_status.get_rect(center=(planta.x, planta.y + tamanho + 20))
    tela.blit(texto_status, texto_pos)

def desenhar_irrigador(tela, pos):
    pygame.draw.rect(tela, AZUL, (pos[0] - 5, pos[1] - 25, 10, 10))

def desenhar_colhedor(tela, pos):
    pygame.draw.rect(tela, AMARELO, (pos[0] - 5, pos[1] - 35, 10, 10))

def desenhar_hud(tela, fonte, acao_irrigador, acao_colhedor, leitura_sensor,
                 colhidas, mortas, tempo_passado):
    pygame.draw.rect(tela, (230, 230, 230), (800, 0, 200, 600))
    tela.blit(fonte.render("INFORMAÇÕES DOS AGENTES:", True, PRETO), (810, 10))
    
    tela.blit(fonte.render("Irrigador:", True, AZUL), (810, 40))
    tela.blit(fonte.render(acao_irrigador, True, PRETO), (810, 60))
    
    tela.blit(fonte.render("Colhedor:", True, AMARELO), (810, 100))
    tela.blit(fonte.render(acao_colhedor, True, PRETO), (810, 120))
    
    tela.blit(fonte.render("Sensor:", True, CINZA), (810, 160))
    tela.blit(fonte.render(leitura_sensor, True, PRETO), (810, 180))
    
    tela.blit(fonte.render(f"Plantas Colhidas: {colhidas}", True, PRETO), (810, 220))
    tela.blit(fonte.render(f"Plantas Mortas: {mortas}", True, PRETO), (810, 240))
    tela.blit(fonte.render(f"Tempo: {tempo_passado}s", True, PRETO), (810, 270))
    tela.blit(fonte.render(f"M - Maturidade da planta(%)", True, LEGENDA), (810, 300))
    tela.blit(fonte.render(f"A - Agua(%)", True, LEGENDA), (810, 320))
