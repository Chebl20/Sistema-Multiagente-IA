import pygame
import math

# Cores melhoradas
CORES = {
    'VERDE_SAUDAVEL': (46, 204, 64),
    'VERDE_JOVEM': (120, 255, 120),
    'VERDE_MADURO': (0, 128, 0),
    'AZUL_AGUA': (74, 144, 226),
    'AZUL_ESCURO': (28, 107, 201),
    'AMARELO_COLHEITA': (255, 220, 0),
    'AMARELO_ESCURO': (218, 165, 32),
    'CINZA_MORTA': (108, 108, 108),
    'CINZA_COLETADA': (169, 169, 169),
    'CINZA_CLARO': (240, 240, 240),
    'PRETO': (0, 0, 0),
    'BRANCO': (255, 255, 255),
    'VERMELHO': (231, 76, 60),
    'VERDE_LEGENDA': (39, 174, 96),
    'ROXO': (155, 89, 182),
    'LARANJA': (230, 126, 34)
}

def desenhar_planta_melhorada(tela, planta, fonte, tempo_atual):
    """Desenha planta com animações e detalhes visuais aprimorados"""
    
    # Animação de pulsação para plantas vivas
    pulso = 1.0
    if not planta.morta and not planta.coletada:
        pulso = 1.0 + 0.1 * math.sin(tempo_atual * 0.005 + planta.x * 0.01)
    
    # Determina cor e tamanho baseado no estado
    if planta.morta:
        cor_principal = CORES['CINZA_MORTA']
        cor_borda = CORES['PRETO']
        tamanho_base = 8
    elif planta.coletada:
        cor_principal = CORES['CINZA_COLETADA']
        cor_borda = CORES['CINZA_MORTA']
        tamanho_base = 6
    else:
        # Cor baseada na maturidade
        if planta.maturidade < 30:
            cor_principal = CORES['VERDE_JOVEM']
        elif planta.maturidade < 70:
            cor_principal = CORES['VERDE_SAUDAVEL']
        else:
            cor_principal = CORES['VERDE_MADURO']
        cor_borda = CORES['VERDE_MADURO']
        tamanho_base = int(8 + planta.maturidade / 12)
    
    tamanho = int(tamanho_base * pulso)
    
    # Desenha sombra
    pygame.draw.circle(tela, (0, 0, 0, 50), (planta.x + 2, planta.y + 2), tamanho)
    
    # Desenha borda da planta
    pygame.draw.circle(tela, cor_borda, (planta.x, planta.y), tamanho + 2)
    
    # Desenha corpo da planta
    pygame.draw.circle(tela, cor_principal, (planta.x, planta.y), tamanho)
    
    # Adiciona brilho se planta estiver madura
    if not planta.morta and not planta.coletada and planta.maturidade > 80:
        for i in range(3):
            alpha = 100 - (i * 30)
            s = pygame.Surface((tamanho * 2, tamanho * 2))
            s.set_alpha(alpha)
            pygame.draw.circle(s, CORES['AMARELO_COLHEITA'], (tamanho, tamanho), tamanho - i * 2)
            tela.blit(s, (planta.x - tamanho, planta.y - tamanho))
    
    # Barra de água aprimorada
    barra_largura = 30
    barra_altura = 6
    barra_x = planta.x - barra_largura // 2
    barra_y = planta.y + tamanho + 8
    
    # Fundo da barra
    pygame.draw.rect(tela, CORES['CINZA_MORTA'], (barra_x, barra_y, barra_largura, barra_altura))
    
    # Preenchimento da barra de água
    agua_largura = int((planta.agua / 100) * barra_largura)
    if planta.agua > 60:
        cor_agua = CORES['AZUL_AGUA']
    elif planta.agua > 30:
        cor_agua = CORES['AZUL_ESCURO']
    else:
        cor_agua = CORES['VERMELHO']
    
    if agua_largura > 0:
        pygame.draw.rect(tela, cor_agua, (barra_x, barra_y, agua_largura, barra_altura))
    
    # Borda da barra
    pygame.draw.rect(tela, CORES['PRETO'], (barra_x, barra_y, barra_largura, barra_altura), 1)
    
    # Barra de maturidade
    barra_y_mat = barra_y + barra_altura + 2
    mat_largura = int((planta.maturidade / 100) * barra_largura)
    
    # Fundo da barra de maturidade
    pygame.draw.rect(tela, CORES['CINZA_MORTA'], (barra_x, barra_y_mat, barra_largura, barra_altura))
    
    # Preenchimento da barra de maturidade
    if mat_largura > 0:
        if planta.maturidade >= 100:
            cor_mat = CORES['AMARELO_COLHEITA']
        else:
            cor_mat = CORES['VERDE_SAUDAVEL']
        pygame.draw.rect(tela, cor_mat, (barra_x, barra_y_mat, mat_largura, barra_altura))
    
    # Borda da barra de maturidade
    pygame.draw.rect(tela, CORES['PRETO'], (barra_x, barra_y_mat, barra_largura, barra_altura), 1)
    
    # Texto de status compacto
    if planta.morta:
        status = "MORTA"
        cor_texto = CORES['VERMELHO']
    elif planta.coletada:
        status = "COLETADA"
        cor_texto = CORES['CINZA_MORTA']
    elif planta.maturidade >= 100:
        status = "PRONTA!"
        cor_texto = CORES['AMARELO_ESCURO']
    else:
        status = f"{int(planta.maturidade)}%"
        cor_texto = CORES['PRETO']
    
    texto_status = fonte.render(status, True, cor_texto)
    texto_rect = texto_status.get_rect(center=(planta.x, planta.y + tamanho + 25))
    tela.blit(texto_status, texto_rect)

def desenhar_agente_melhorado(tela, pos, tipo, ativo=False, fonte_pequena=None):
    """Desenha agentes com animações, indicadores visuais e localização precisa"""
    x, y = pos
# desloca o agente para ficar acima da planta, não por cima dela
    OFFSET_Y = 20  
    y -= OFFSET_Y
    
    if tipo == "irrigador":
        cor_principal = CORES['AZUL_AGUA']
        cor_secundaria = CORES['AZUL_ESCURO']
        cor_trail = CORES['AZUL_AGUA']
        simbolo = "💧"
        nome = "IRRIGADOR"
    else:  # colhedor
        cor_principal = CORES['AMARELO_COLHEITA']
        cor_secundaria = CORES['AMARELO_ESCURO']
        cor_trail = CORES['AMARELO_COLHEITA']
        simbolo = "🌾"
        nome = "COLHEDOR"
    
    # Rastro/trilha do movimento (linhas pontilhadas em cruz)
    for i in range(-20, 21, 5):
        alpha = max(0, 100 - abs(i) * 3)
        if alpha > 20:
            # Linhas horizontais
            pygame.draw.circle(tela, (*cor_trail, alpha), (x + i, y), 2)
            # Linhas verticais
            pygame.draw.circle(tela, (*cor_trail, alpha), (x, y + i), 2)
    
    # Círculo de área de ação (raio de alcance)
    if ativo:
        pygame.draw.circle(tela, (*cor_principal, 30), (x, y), 40, 2)
        pygame.draw.circle(tela, (*cor_principal, 15), (x, y), 25, 1)
    
    # Efeito de atividade (aura pulsante)
    tamanho = 12
    if ativo:
        tamanho = 16
        # Aura pulsante mais visível
        for i in range(4):
            alpha = 80 - (i * 20)
            raio = 20 + i * 8
            s = pygame.Surface((raio * 2, raio * 2))
            s.set_alpha(alpha)
            pygame.draw.circle(s, cor_principal, (raio, raio), raio, 3)
            tela.blit(s, (x - raio, y - raio))
    
    # Sombra do agente
    pygame.draw.circle(tela, (50, 50, 50, 100), (x + 3, y + 3), tamanho + 2)
    
    # Corpo principal do agente (formato mais distintivo)
    pygame.draw.circle(tela, CORES['PRETO'], (x, y), tamanho + 3)  # Borda preta
    pygame.draw.circle(tela, cor_secundaria, (x, y), tamanho + 1)  # Borda colorida
    pygame.draw.circle(tela, cor_principal, (x, y), tamanho)       # Corpo principal
    
    # Centro brilhante
    pygame.draw.circle(tela, CORES['BRANCO'], (x - 3, y - 3), 3)
    
    # Indicador de direção/orientação
    if tipo == "irrigador":
        # Desenha gotas d'água
        for i, offset in enumerate([(0, -20), (-8, -15), (8, -15)]):
            gota_x, gota_y = x + offset[0], y + offset[1]
            pygame.draw.circle(tela, CORES['AZUL_AGUA'], (gota_x, gota_y), 2)
    else:
        # Desenha símbolo de colheita
        pontos = [
            (x, y - 20),
            (x - 6, y - 12),
            (x + 6, y - 12),
            (x, y - 16)
        ]
        pygame.draw.polygon(tela, CORES['AMARELO_ESCURO'], pontos)
    
    # Nome e coordenadas do agente
    if fonte_pequena:
        # Nome do agente
        texto_nome = fonte_pequena.render(nome, True, CORES['PRETO'])
        nome_rect = texto_nome.get_rect(center=(x, y + tamanho + 8))
        
        # Fundo do texto para melhor legibilidade
        pygame.draw.rect(tela, CORES['BRANCO'], nome_rect.inflate(4, 2))
        pygame.draw.rect(tela, cor_secundaria, nome_rect.inflate(4, 2), 1)
        tela.blit(texto_nome, nome_rect)
        
        # Coordenadas precisas
        coord_texto = f"({x}, {y})"
        texto_coord = fonte_pequena.render(coord_texto, True, cor_secundaria)
        coord_rect = texto_coord.get_rect(center=(x, y + tamanho + 22))
        
        # Fundo das coordenadas
        pygame.draw.rect(tela, CORES['BRANCO'], coord_rect.inflate(2, 1))
        tela.blit(texto_coord, coord_rect)
    
    # Linha conectora para mostrar posição exata
    pygame.draw.line(tela, cor_secundaria, (x, y + tamanho), (x, y + tamanho + 5), 2)

def desenhar_mira_posicao(tela, pos, cor, tamanho=15):
    """Desenha uma mira para indicar posição exata"""
    x, y = pos
    
    # Mira em cruz
    pygame.draw.line(tela, cor, (x - tamanho, y), (x + tamanho, y), 2)
    pygame.draw.line(tela, cor, (x, y - tamanho), (x, y + tamanho), 2)
    
    # Círculo central
    pygame.draw.circle(tela, cor, (x, y), 3)
    pygame.draw.circle(tela, CORES['BRANCO'], (x, y), 1)

def desenhar_grid_coordenadas(tela, largura, altura, fonte_pequena, tamanho_grid=100):
    """Desenha grid com coordenadas para referência"""
    cor_grid = (180, 180, 180)
    cor_texto = (120, 120, 120)
    
    # Linhas verticais com coordenadas
    for x in range(0, largura, tamanho_grid):
        pygame.draw.line(tela, cor_grid, (x, 0), (x, altura), 1)
        if x > 0:  # Não desenha no x=0
            texto = fonte_pequena.render(str(x), True, cor_texto)
            tela.blit(texto, (x + 2, 2))
    
    # Linhas horizontais com coordenadas
    for y in range(0, altura, tamanho_grid):
        pygame.draw.line(tela, cor_grid, (0, y), (largura, y), 1)
        if y > 0:  # Não desenha no y=0
            texto = fonte_pequena.render(str(y), True, cor_texto)
            tela.blit(texto, (2, y + 2))

def desenhar_hud_melhorado(tela, fonte, fonte_pequena, acao_irrigador, acao_colhedor, 
                           leitura_sensor, colhidas, mortas, tempo_passado, total_plantas,
                           pos_irrigador=None, pos_colhedor=None, plantas_vivas=None):
    """HUD sem emojis, dead-bar ajustada e texto reposicionado para visibilidade"""

    # Painel principal (220×altura suficiente)
    painel_x, painel_w = 780, 220
    pygame.draw.rect(tela, CORES['CINZA_CLARO'], (painel_x, 0, painel_w, 600))
    pygame.draw.rect(tela, CORES['PRETO'],       (painel_x, 0, painel_w, 600), 2)

    y_pos = 15
    tela.blit(fonte.render("SISTEMA DE MONITORAMENTO", True, CORES['PRETO']),
              (painel_x+5, y_pos))
    y_pos += 35
    pygame.draw.line(tela, CORES['PRETO'],
                     (painel_x+5, y_pos), (painel_x+painel_w-5, y_pos), 2)
    y_pos += 15

    # AGENTES IA
    tela.blit(fonte.render("AGENTES IA", True, CORES['ROXO']), (painel_x+5, y_pos))
    y_pos += 25

    # Irrigador
    pygame.draw.circle(tela, CORES['AZUL_AGUA'], (painel_x+10, y_pos+8), 6)
    tela.blit(fonte_pequena.render("Irrigador:", True, CORES['PRETO']),
              (painel_x+25, y_pos))
    if pos_irrigador:
        tela.blit(fonte_pequena.render(f"Pos: {pos_irrigador}", True, CORES['AZUL_ESCURO']),
                  (painel_x+25, y_pos+15))
        y_pos += 15
    tela.blit(fonte_pequena.render(acao_irrigador, True, CORES['AZUL_ESCURO']),
              (painel_x+25, y_pos+30))
    y_pos += 45

    # Colhedor
    pygame.draw.circle(tela, CORES['AMARELO_COLHEITA'], (painel_x+10, y_pos+8), 6)
    tela.blit(fonte_pequena.render("Colhedor:", True, CORES['PRETO']),
              (painel_x+25, y_pos))
    if pos_colhedor:
        tela.blit(fonte_pequena.render(f"Pos: {pos_colhedor}", True, CORES['AMARELO_ESCURO']),
                  (painel_x+25, y_pos+15))
        y_pos += 15
    tela.blit(fonte_pequena.render(acao_colhedor, True, CORES['AMARELO_ESCURO']),
              (painel_x+25, y_pos+30))
    y_pos += 45

    # Sensor
    pygame.draw.circle(tela, CORES['CINZA_MORTA'], (painel_x+10, y_pos+8), 6)
    tela.blit(fonte_pequena.render("Sensor:", True, CORES['PRETO']),
              (painel_x+25, y_pos))
    tela.blit(fonte_pequena.render(leitura_sensor, True, CORES['PRETO']),
              (painel_x+25, y_pos+30))
    y_pos += 50

    pygame.draw.line(tela, CORES['PRETO'],
                     (painel_x+5, y_pos), (painel_x+painel_w-5, y_pos), 1)
    y_pos += 15

    # MÉTRICAS
    tela.blit(fonte.render("MÉTRICAS", True, CORES['VERDE_LEGENDA']),
              (painel_x+5, y_pos))
    y_pos += 30

    # Novo: viva = total de plantas menos as mortas
    largura_barra = painel_w - 30
    altura_barra = 15

    def draw_bar(label, count, color, y):
        tela.blit(fonte_pequena.render(f"{label}: {count}", True, color),
                  (painel_x+5, y))
        pygame.draw.rect(tela, CORES['CINZA_MORTA'],
                         (painel_x+5, y+20, largura_barra, altura_barra))
        if total_plantas > 0:
            largura = min(int((count / total_plantas) * largura_barra), largura_barra)
            pygame.draw.rect(tela, color,
                             (painel_x+5, y+20, largura, altura_barra))
        pygame.draw.rect(tela, CORES['PRETO'],
                         (painel_x+5, y+20, largura_barra, altura_barra), 1)

    # Desenha as barras: Vivas (agora total-mortas), Colhidas e Mortas
    draw_bar("Vivas", plantas_vivas, CORES['VERDE_SAUDAVEL'], y_pos)
    y_pos += 45
    draw_bar("Colhidas", colhidas, CORES['AMARELO_ESCURO'], y_pos)
    y_pos += 45
    draw_bar("Mortas", mortas, CORES['VERMELHO'], y_pos)
    y_pos += 45

    # Taxa de sucesso
    if (colhidas + mortas) > 0:
        taxa = (colhidas / (colhidas + mortas)) * 100
        cor_taxa = (CORES['VERDE_SAUDAVEL'] if taxa > 70 else
                    CORES['LARANJA']       if taxa > 40 else
                    CORES['VERMELHO'])
        tela.blit(fonte_pequena.render(f"Taxa Sucesso: {taxa:.1f}%", True, cor_taxa),
                  (painel_x+5, y_pos))
        y_pos += 30

    # Tempo
    minutos, segundos = divmod(tempo_passado, 60)
    tela.blit(fonte.render(f"Tempo: {minutos:02d}:{segundos:02d}", True, CORES['PRETO']),
              (painel_x+5, y_pos))
    y_pos += 40

    pygame.draw.line(tela, CORES['PRETO'],
                     (painel_x+5, y_pos), (painel_x+painel_w-5, y_pos), 1)
    y_pos += 15

    # LEGENDA sem emojis
    tela.blit(fonte.render("LEGENDA", True, CORES['PRETO']), (painel_x+5, y_pos))
    y_pos += 25
    legendas = [
        ("Nível de Água",  CORES['AZUL_AGUA']),
        ("Maturidade",      CORES['VERDE_SAUDAVEL']),
        ("Baixa Água",      CORES['VERMELHO']),
        ("Pronta Colheita", CORES['AMARELO_COLHEITA']),
        ("Posição Agentes", CORES['PRETO'])
    ]
    for texto, cor in legendas:
        tela.blit(fonte_pequena.render(texto, True, cor), (painel_x+5, y_pos))
        y_pos += 18

def desenhar_grid_fundo(tela, largura, altura, tamanho_grid=50):
    """Desenha uma grade sutil no fundo para melhor orientação visual"""
    cor_grid = (200, 200, 200)
    
    for x in range(0, largura, tamanho_grid):
        pygame.draw.line(tela, cor_grid, (x, 0), (x, altura), 1)
    
    for y in range(0, altura, tamanho_grid):
        pygame.draw.line(tela, cor_grid, (0, y), (largura, y), 1)

def desenhar_estatisticas_tempo_real(tela, fonte_pequena, plantas, x_offset=10, y_offset=550):
    """Desenha estatísticas em tempo real na parte inferior da tela"""
    
    # Calcula estatísticas
    total = len(plantas)
    vivas = sum(1 for p in plantas if not p.morta and not p.coletada)
    colhidas = sum(1 for p in plantas if p.coletada)
    mortas = sum(1 for p in plantas if p.morta)
    
    if vivas > 0:
        agua_media = sum(p.agua for p in plantas if not p.morta and not p.coletada) / vivas
        maturidade_media = sum(p.maturidade for p in plantas if not p.morta and not p.coletada) / vivas
    else:
        agua_media = 0
        maturidade_media = 0
    
    # Fundo semitransparente
    s = pygame.Surface((760, 45))
    s.set_alpha(180)
    s.fill(CORES['CINZA_CLARO'])
    tela.blit(s, (x_offset, y_offset))
    
    # Textos das estatísticas
    stats = [
        f"Total: {total}",
        f"Vivas: {vivas}",
        f"Colhidas: {colhidas}",
        f"Mortas: {mortas}",
        f"Água Média: {agua_media:.1f}%",
        f"Maturidade Média: {maturidade_media:.1f}%"
    ]
    
    x_pos = x_offset + 10
    for i, stat in enumerate(stats):
        if i == 3:  # Nova linha após "Mortas"
            x_pos = x_offset + 10
            y_offset += 20
        
        cor_texto = CORES['PRETO']
        if "Mortas:" in stat and mortas > 0:
            cor_texto = CORES['VERMELHO']
        elif "Colhidas:" in stat and colhidas > 0:
            cor_texto = CORES['VERDE_SAUDAVEL']
        
        texto = fonte_pequena.render(stat, True, cor_texto)
        tela.blit(texto, (x_pos, y_offset))
        x_pos += texto.get_width() + 20

# Funções auxiliares para integração
def obter_tempo_pygame():
    """Retorna o tempo atual do pygame para animações"""
    return pygame.time.get_ticks()

def criar_fontes():
    """Cria e retorna as fontes necessárias"""
    pygame.font.init()
    fonte_principal = pygame.font.Font(None, 16)
    fonte_pequena = pygame.font.Font(None, 14)
    return fonte_principal, fonte_pequena