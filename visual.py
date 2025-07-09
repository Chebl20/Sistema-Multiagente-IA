import pygame
import math

# Cores aprimoradas com mais variações
CORES = {
    'VERDE_SAUDAVEL': (46, 204, 64),
    'VERDE_JOVEM': (120, 255, 120),
    'VERDE_MADURO': (0, 128, 0),
    'VERDE_NEON': (57, 255, 20),
    'AZUL_AGUA': (74, 144, 226),
    'AZUL_ESCURO': (28, 107, 201),
    'AZUL_CLARO': (135, 206, 235),
    'AMARELO_COLHEITA': (255, 220, 0),
    'AMARELO_ESCURO': (218, 165, 32),
    'AMARELO_DOURADO': (255, 215, 0),
    'CINZA_MORTA': (108, 108, 108),
    'CINZA_COLETADA': (169, 169, 169),
    'CINZA_CLARO': (240, 240, 240),
    'PRETO': (0, 0, 0),
    'BRANCO': (255, 255, 255),
    'VERMELHO': (231, 76, 60),
    'VERMELHO_ESCURO': (155, 39, 39),
    'VERDE_LEGENDA': (39, 174, 96),
    'ROXO': (155, 89, 182),
    'ROXO_ESCURO': (102, 51, 153),
    'LARANJA': (230, 126, 34),
    'ROSA': (255, 182, 193),
    'DOURADO': (255, 215, 0)
}

def criar_superficie_com_alpha(tamanho, alpha=255):
    """Cria uma superfície com canal alpha para efeitos de transparência"""
    surface = pygame.Surface(tamanho, pygame.SRCALPHA)
    surface.set_alpha(alpha)
    return surface

def desenhar_gradiente_circular(surface, centro, raio, cor_interna, cor_externa, alpha=255):
    """Desenha um gradiente circular suave"""
    x, y = centro
    for r in range(raio, 0, -1):
        # Interpola entre cores
        ratio = r / raio
        cor_atual = [
            int(cor_interna[i] * (1 - ratio) + cor_externa[i] * ratio)
            for i in range(3)
        ]
        
        # Cria superfície temporária com alpha
        temp_surface = criar_superficie_com_alpha((r * 2, r * 2), alpha)
        pygame.draw.circle(temp_surface, cor_atual, (r, r), r)
        surface.blit(temp_surface, (x - r, y - r))

def desenhar_barra_gradiente(surface, rect, cor_inicio, cor_fim, porcentagem, vertical=False):
    """Desenha uma barra com gradiente e animação de preenchimento"""
    x, y, w, h = rect
    
    # Fundo da barra com gradiente sutil
    for i in range(w if not vertical else h):
        pos = i / (w if not vertical else h)
        cor_fundo = [
            int(CORES['CINZA_MORTA'][j] * (1 - pos * 0.3) + CORES['CINZA_CLARO'][j] * (pos * 0.3))
            for j in range(3)
        ]
        
        if vertical:
            pygame.draw.line(surface, cor_fundo, (x, y + i), (x + w, y + i))
        else:
            pygame.draw.line(surface, cor_fundo, (x + i, y), (x + i, y + h))
    
    # Preenchimento com gradiente
    tamanho_preenchimento = int((porcentagem / 100) * (w if not vertical else h))
    
    for i in range(tamanho_preenchimento):
        pos = i / (tamanho_preenchimento if tamanho_preenchimento > 0 else 1)
        cor_atual = [
            int(cor_inicio[j] * (1 - pos) + cor_fim[j] * pos)
            for j in range(3)
        ]
        
        if vertical:
            pygame.draw.line(surface, cor_atual, (x, y + h - i - 1), (x + w, y + h - i - 1))
        else:
            pygame.draw.line(surface, cor_atual, (x + i, y), (x + i, y + h))

def desenhar_planta_melhorada(tela, planta, fonte, tempo_atual):
    """Desenha planta com animações e detalhes visuais aprimorados"""
    
    # Animação de pulsação mais suave para plantas vivas
    pulso = 1.0
    brilho_extra = 0
    if not planta.morta and not planta.coletada:
        pulso = 1.0 + 0.08 * math.sin(tempo_atual * 0.003 + planta.x * 0.01)
        brilho_extra = int(20 * math.sin(tempo_atual * 0.004 + planta.y * 0.01))
    
    # Determina cor e tamanho baseado no estado
    if planta.morta:
        cor_principal = CORES['CINZA_MORTA']
        cor_borda = CORES['PRETO']
        cor_interna = CORES['CINZA_COLETADA']
        tamanho_base = 8
    elif planta.coletada:
        cor_principal = CORES['CINZA_COLETADA']
        cor_borda = CORES['CINZA_MORTA']
        cor_interna = CORES['CINZA_CLARO']
        tamanho_base = 6
    else:
        # Cor baseada na maturidade com transições suaves
        if planta.maturidade < 30:
            cor_principal = CORES['VERDE_JOVEM']
            cor_interna = CORES['VERDE_NEON']
        elif planta.maturidade < 70:
            cor_principal = CORES['VERDE_SAUDAVEL']
            cor_interna = CORES['VERDE_JOVEM']
        else:
            cor_principal = CORES['VERDE_MADURO']
            cor_interna = CORES['VERDE_SAUDAVEL']
        cor_borda = CORES['VERDE_MADURO']
        tamanho_base = int(8 + planta.maturidade / 12)
    
    tamanho = int(tamanho_base * pulso)
    
    # Sombra com múltiplas camadas para efeito mais realista
    for i in range(3):
        alpha = 60 - (i * 20)
        shadow_surface = criar_superficie_com_alpha((tamanho * 2 + 6, tamanho * 2 + 6), alpha)
        pygame.draw.circle(shadow_surface, CORES['PRETO'], (tamanho + 3, tamanho + 3), tamanho + i)
        tela.blit(shadow_surface, (planta.x - tamanho - 3, planta.y - tamanho - 3))
    
    # Aura luminosa para plantas saudáveis
    if not planta.morta and not planta.coletada and planta.maturidade > 50:
        aura_surface = criar_superficie_com_alpha((tamanho * 4, tamanho * 4), 30)
        desenhar_gradiente_circular(aura_surface, (tamanho * 2, tamanho * 2), tamanho * 2, 
                                   cor_interna, cor_principal, 30)
        tela.blit(aura_surface, (planta.x - tamanho * 2, planta.y - tamanho * 2))
    
    # Corpo da planta com gradiente
    planta_surface = criar_superficie_com_alpha((tamanho * 2 + 6, tamanho * 2 + 6))
    
    # Borda externa
    pygame.draw.circle(planta_surface, cor_borda, (tamanho + 3, tamanho + 3), tamanho + 2)
    
    # Gradiente do corpo principal
    desenhar_gradiente_circular(planta_surface, (tamanho + 3, tamanho + 3), tamanho + 1, 
                               cor_interna, cor_principal)
    
    # Brilho central
    if not planta.morta and not planta.coletada:
        highlight_color = [min(255, c + brilho_extra) for c in cor_interna]
        pygame.draw.circle(planta_surface, highlight_color, (tamanho - 2, tamanho + 1), max(2, tamanho // 3))
    
    tela.blit(planta_surface, (planta.x - tamanho - 3, planta.y - tamanho - 3))
    
    # Efeito especial para plantas prontas para colheita
    if not planta.morta and not planta.coletada and planta.maturidade >= 100:
        # Partículas douradas
        for i in range(5):
            angle = (tempo_atual * 0.002 + i * 72) % 360
            dist = 25 + 5 * math.sin(tempo_atual * 0.003 + i)
            part_x = planta.x + dist * math.cos(math.radians(angle))
            part_y = planta.y + dist * math.sin(math.radians(angle))
            
            sparkle_surface = criar_superficie_com_alpha((8, 8), 150)
            pygame.draw.circle(sparkle_surface, CORES['DOURADO'], (4, 4), 3)
            pygame.draw.circle(sparkle_surface, CORES['AMARELO_COLHEITA'], (4, 4), 1)
            tela.blit(sparkle_surface, (int(part_x - 4), int(part_y - 4)))
    
    # Barras de status aprimoradas
    barra_largura = 32
    barra_altura = 8
    barra_x = planta.x - barra_largura // 2
    barra_y = planta.y + tamanho + 12
    
    # Barra de água com gradiente
    agua_rect = (barra_x, barra_y, barra_largura, barra_altura)
    if planta.agua > 60:
        cor_agua_inicio = CORES['AZUL_CLARO']
        cor_agua_fim = CORES['AZUL_AGUA']
    elif planta.agua > 30:
        cor_agua_inicio = CORES['AZUL_AGUA']
        cor_agua_fim = CORES['AZUL_ESCURO']
    else:
        cor_agua_inicio = CORES['LARANJA']
        cor_agua_fim = CORES['VERMELHO']
    
    desenhar_barra_gradiente(tela, agua_rect, cor_agua_inicio, cor_agua_fim, planta.agua)
    
    # Borda da barra de água
    pygame.draw.rect(tela, CORES['PRETO'], agua_rect, 2)
    
    # Barra de maturidade
    barra_y_mat = barra_y + barra_altura + 4
    mat_rect = (barra_x, barra_y_mat, barra_largura, barra_altura)
    
    if planta.maturidade >= 100:
        cor_mat_inicio = CORES['AMARELO_DOURADO']
        cor_mat_fim = CORES['AMARELO_COLHEITA']
    else:
        cor_mat_inicio = CORES['VERDE_JOVEM']
        cor_mat_fim = CORES['VERDE_SAUDAVEL']
    
    desenhar_barra_gradiente(tela, mat_rect, cor_mat_inicio, cor_mat_fim, planta.maturidade)
    
    # Borda da barra de maturidade
    pygame.draw.rect(tela, CORES['PRETO'], mat_rect, 2)
    
    # Texto de status com fundo semitransparente
    if planta.morta:
        status = "MORTA"
        cor_texto = CORES['VERMELHO']
        cor_fundo = CORES['PRETO']
    elif planta.coletada:
        status = "COLETADA"
        cor_texto = CORES['CINZA_MORTA']
        cor_fundo = CORES['CINZA_CLARO']
    elif planta.maturidade >= 100:
        status = "PRONTA!"
        cor_texto = CORES['DOURADO']
        cor_fundo = CORES['AMARELO_ESCURO']
    else:
        status = f"{int(planta.maturidade)}%"
        cor_texto = CORES['VERDE_MADURO']
        cor_fundo = CORES['VERDE_JOVEM']
    
    texto_status = fonte.render(status, True, cor_texto)
    texto_rect = texto_status.get_rect(center=(planta.x, planta.y + tamanho + 32))
    
    # Fundo do texto
    fundo_rect = texto_rect.inflate(8, 4)
    fundo_surface = criar_superficie_com_alpha((fundo_rect.width, fundo_rect.height), 180)
    fundo_surface.fill(cor_fundo)
    tela.blit(fundo_surface, fundo_rect)
    
    tela.blit(texto_status, texto_rect)

def desenhar_agente_melhorado(tela, pos, tipo, ativo=False, fonte_pequena=None):
    """Desenha agentes com animações, indicadores visuais e localização precisa"""
    x, y = pos
    # Desloca o agente para ficar acima da planta, não por cima dela
    OFFSET_Y = 20  
    y -= OFFSET_Y
    
    tempo_atual = pygame.time.get_ticks()
    
    if tipo == "irrigador":
        cor_principal = CORES['AZUL_AGUA']
        cor_secundaria = CORES['AZUL_ESCURO']
        cor_trail = CORES['AZUL_CLARO']
        cor_aura = CORES['AZUL_AGUA']
        nome = "IRRIGADOR"
    else:  # colhedor
        cor_principal = CORES['AMARELO_COLHEITA']
        cor_secundaria = CORES['AMARELO_ESCURO']
        cor_trail = CORES['AMARELO_DOURADO']
        cor_aura = CORES['AMARELO_COLHEITA']
        nome = "COLHEDOR"
    
    # Rastro/trilha do movimento com efeito de fade
    if ativo:
        for i in range(-30, 31, 4):
            alpha = max(0, 80 - abs(i) * 2)
            if alpha > 10:
                trail_surface = criar_superficie_com_alpha((6, 6), alpha)
                pygame.draw.circle(trail_surface, cor_trail, (3, 3), 2)
                tela.blit(trail_surface, (x + i - 3, y - 3))
                tela.blit(trail_surface, (x - 3, y + i - 3))
    
    # Área de ação com ondas concêntricas
    if ativo:
        for i in range(3):
            raio = 35 + i * 10
            alpha = 40 - (i * 10)
            onda_surface = criar_superficie_com_alpha((raio * 2, raio * 2), alpha)
            pygame.draw.circle(onda_surface, cor_aura, (raio, raio), raio, 2)
            tela.blit(onda_surface, (x - raio, y - raio))
    
    # Efeito de atividade com pulsação
    tamanho = 14
    if ativo:
        pulso = 1.0 + 0.3 * math.sin(tempo_atual * 0.008)
        tamanho = int(14 * pulso)
        
        # Aura pulsante mais sofisticada
        for i in range(4):
            alpha = 100 - (i * 25)
            raio = int((25 + i * 10) * pulso)
            aura_surface = criar_superficie_com_alpha((raio * 2, raio * 2), alpha)
            desenhar_gradiente_circular(aura_surface, (raio, raio), raio, 
                                       cor_aura, cor_principal, alpha)
            tela.blit(aura_surface, (x - raio, y - raio))
    
    # Sombra em múltiplas camadas
    for i in range(3):
        alpha = 80 - (i * 25)
        shadow_surface = criar_superficie_com_alpha((tamanho * 2 + 8, tamanho * 2 + 8), alpha)
        pygame.draw.circle(shadow_surface, CORES['PRETO'], (tamanho + 4, tamanho + 4), tamanho + i)
        tela.blit(shadow_surface, (x - tamanho - 4, y - tamanho - 4))
    
    # Corpo principal do agente com gradiente
    agente_surface = criar_superficie_com_alpha((tamanho * 2 + 8, tamanho * 2 + 8))
    
    # Borda externa
    pygame.draw.circle(agente_surface, CORES['PRETO'], (tamanho + 4, tamanho + 4), tamanho + 3)
    
    # Borda colorida
    pygame.draw.circle(agente_surface, cor_secundaria, (tamanho + 4, tamanho + 4), tamanho + 1)
    
    # Corpo principal com gradiente
    desenhar_gradiente_circular(agente_surface, (tamanho + 4, tamanho + 4), tamanho, 
                               CORES['BRANCO'], cor_principal)
    
    # Centro brilhante animado
    brilho_size = max(3, int(6 + 2 * math.sin(tempo_atual * 0.005)))
    pygame.draw.circle(agente_surface, CORES['BRANCO'], (tamanho - 2, tamanho + 2), brilho_size)
    
    tela.blit(agente_surface, (x - tamanho - 4, y - tamanho - 4))
    
    # Indicador de direção/orientação animado
    if tipo == "irrigador":
        # Desenha gotas d'água animadas
        for i, offset in enumerate([(0, -25), (-10, -20), (10, -20)]):
            gota_x, gota_y = x + offset[0], y + offset[1]
            animacao_offset = 3 * math.sin(tempo_atual * 0.01 + i * 2)
            gota_y += animacao_offset
            
            # Gota com gradiente
            gota_surface = criar_superficie_com_alpha((8, 8), 200)
            pygame.draw.circle(gota_surface, CORES['AZUL_CLARO'], (4, 4), 3)
            pygame.draw.circle(gota_surface, CORES['BRANCO'], (3, 3), 1)
            tela.blit(gota_surface, (int(gota_x - 4), int(gota_y - 4)))
    else:
        # Desenha símbolo de colheita com animação
        rotacao = tempo_atual * 0.003
        for i in range(4):
            angle = rotacao + i * 90
            spike_x = x + 8 * math.cos(math.radians(angle))
            spike_y = y - 20 + 8 * math.sin(math.radians(angle))
            
            spike_surface = criar_superficie_com_alpha((6, 6), 180)
            pygame.draw.circle(spike_surface, CORES['AMARELO_ESCURO'], (3, 3), 2)
            tela.blit(spike_surface, (int(spike_x - 3), int(spike_y - 3)))
    
    # Nome e coordenadas do agente com fundo estilizado
    if fonte_pequena:
        # Nome do agente
        texto_nome = fonte_pequena.render(nome, True, CORES['BRANCO'])
        nome_rect = texto_nome.get_rect(center=(x, y + tamanho + 12))
        
        # Fundo do texto com gradiente
        fundo_nome = nome_rect.inflate(8, 4)
        fundo_surface = criar_superficie_com_alpha((fundo_nome.width, fundo_nome.height), 200)
        fundo_surface.fill(cor_secundaria)
        tela.blit(fundo_surface, fundo_nome)
        
        # Borda do fundo
        pygame.draw.rect(tela, cor_principal, fundo_nome, 2)
        tela.blit(texto_nome, nome_rect)
        
        # Coordenadas precisas
        coord_texto = f"({x}, {y + OFFSET_Y})"
        texto_coord = fonte_pequena.render(coord_texto, True, cor_secundaria)
        coord_rect = texto_coord.get_rect(center=(x, y + tamanho + 28))
        
        # Fundo das coordenadas
        fundo_coord = coord_rect.inflate(4, 2)
        coord_surface = criar_superficie_com_alpha((fundo_coord.width, fundo_coord.height), 150)
        coord_surface.fill(CORES['BRANCO'])
        tela.blit(coord_surface, fundo_coord)
        tela.blit(texto_coord, coord_rect)
    
    # Linha conectora animada
    linha_y = y + tamanho
    for i in range(8):
        alpha = 200 - (i * 20)
        linha_surface = criar_superficie_com_alpha((4, 2), alpha)
        linha_surface.fill(cor_secundaria)
        tela.blit(linha_surface, (x - 2, linha_y + i * 2))

def desenhar_mira_posicao(tela, pos, cor, tamanho=15):
    """Desenha uma mira para indicar posição exata"""
    x, y = pos
    
    # Mira em cruz com efeito de brilho
    for i in range(3):
        alpha = 255 - (i * 80)
        linha_surface = criar_superficie_com_alpha((tamanho * 2, 4), alpha)
        linha_surface.fill(cor)
        tela.blit(linha_surface, (x - tamanho, y - 2))
        
        linha_surface = criar_superficie_com_alpha((4, tamanho * 2), alpha)
        linha_surface.fill(cor)
        tela.blit(linha_surface, (x - 2, y - tamanho))
    
    # Círculo central com gradiente
    centro_surface = criar_superficie_com_alpha((8, 8))
    desenhar_gradiente_circular(centro_surface, (4, 4), 4, CORES['BRANCO'], cor)
    tela.blit(centro_surface, (x - 4, y - 4))

def desenhar_grid_coordenadas(tela, largura, altura, fonte_pequena, tamanho_grid=100):
    """Desenha grid com coordenadas para referência"""
    cor_grid = (200, 200, 200)
    cor_texto = (100, 100, 100)
    
    # Linhas verticais com efeito de fade
    for x in range(0, largura, tamanho_grid):
        # Linha principal
        pygame.draw.line(tela, cor_grid, (x, 0), (x, altura), 1)
        
        # Linhas secundárias mais sutis
        for sub_x in range(x + tamanho_grid // 4, x + tamanho_grid, tamanho_grid // 4):
            if sub_x < largura:
                pygame.draw.line(tela, (*cor_grid, 100), (sub_x, 0), (sub_x, altura), 1)
        
        if x > 0:
            # Fundo do texto
            texto = fonte_pequena.render(str(x), True, cor_texto)
            texto_rect = texto.get_rect(topleft=(x + 4, 4))
            fundo_surface = criar_superficie_com_alpha((texto_rect.width + 4, texto_rect.height + 2), 150)
            fundo_surface.fill(CORES['BRANCO'])
            tela.blit(fundo_surface, (x + 2, 2))
            tela.blit(texto, texto_rect)
    
    # Linhas horizontais com efeito de fade
    for y in range(0, altura, tamanho_grid):
        # Linha principal
        pygame.draw.line(tela, cor_grid, (0, y), (largura, y), 1)
        
        # Linhas secundárias mais sutis
        for sub_y in range(y + tamanho_grid // 4, y + tamanho_grid, tamanho_grid // 4):
            if sub_y < altura:
                pygame.draw.line(tela, (*cor_grid, 100), (0, sub_y), (largura, sub_y), 1)
        
        if y > 0:
            # Fundo do texto
            texto = fonte_pequena.render(str(y), True, cor_texto)
            texto_rect = texto.get_rect(topleft=(4, y + 4))
            fundo_surface = criar_superficie_com_alpha((texto_rect.width + 4, texto_rect.height + 2), 150)
            fundo_surface.fill(CORES['BRANCO'])
            tela.blit(fundo_surface, (2, y + 2))
            tela.blit(texto, texto_rect)

def desenhar_hud_melhorado(tela, fonte, fonte_pequena, acao_irrigador, acao_colhedor, 
                           leitura_sensor, colhidas, mortas, tempo_passado, total_plantas,
                           pos_irrigador=None, pos_colhedor=None, plantas_vivas=None):
    """HUD com visual moderno e gradientes"""

    # Painel principal com gradiente
    painel_x, painel_w = 780, 220
    painel_rect = (painel_x, 0, painel_w, 600)
    
    # Fundo do painel com gradiente
    for i in range(painel_w):
        ratio = i / painel_w
        cor_atual = [
            int(CORES['CINZA_CLARO'][j] * (1 - ratio) + CORES['BRANCO'][j] * ratio)
            for j in range(3)
        ]
        pygame.draw.line(tela, cor_atual, (painel_x + i, 0), (painel_x + i, 600))
    
    # Borda do painel
    pygame.draw.rect(tela, CORES['PRETO'], painel_rect, 3)
    
    # Linha decorativa superior
    pygame.draw.line(tela, CORES['ROXO'], (painel_x + 5, 5), (painel_x + painel_w - 5, 5), 3)
    pygame.draw.line(tela, CORES['ROXO_ESCURO'], (painel_x + 5, 8), (painel_x + painel_w - 5, 8), 1)

    y_pos = 20
    
    # Título com sombra
    titulo_surface = criar_superficie_com_alpha((painel_w - 10, 25), 200)
    titulo_surface.fill(CORES['ROXO_ESCURO'])
    tela.blit(titulo_surface, (painel_x + 5, y_pos - 5))
    
    texto_titulo = fonte.render("SISTEMA DE MONITORAMENTO", True, CORES['BRANCO'])
    tela.blit(texto_titulo, (painel_x + 8, y_pos))
    y_pos += 35
    
    # Linha separadora com gradiente
    for i in range(painel_w - 10):
        alpha = 255 - abs(i - (painel_w - 10) // 2) * 4
        cor_linha = (*CORES['PRETO'], min(255, alpha))
        pygame.draw.line(tela, CORES['PRETO'], (painel_x + 5 + i, y_pos), (painel_x + 5 + i, y_pos + 2))
    y_pos += 15

    # AGENTES IA com fundo destacado
    agentes_surface = criar_superficie_com_alpha((painel_w - 10, 25), 150)
    agentes_surface.fill(CORES['ROXO'])
    tela.blit(agentes_surface, (painel_x + 5, y_pos - 5))
    
    tela.blit(fonte.render("AGENTES IA", True, CORES['BRANCO']), (painel_x + 8, y_pos))
    y_pos += 25

    # Irrigador com visual aprimorado
    # Círculo com gradiente
    irrigador_surface = criar_superficie_com_alpha((16, 16))
    desenhar_gradiente_circular(irrigador_surface, (8, 8), 8, CORES['AZUL_CLARO'], CORES['AZUL_AGUA'])
    tela.blit(irrigador_surface, (painel_x + 5, y_pos + 3))
    
    tela.blit(fonte_pequena.render("Irrigador:", True, CORES['PRETO']),
              (painel_x + 25, y_pos))
    if pos_irrigador:
        pos_texto = fonte_pequena.render(f"Pos: {pos_irrigador}", True, CORES['AZUL_ESCURO'])
        # Fundo do texto de posição
        pos_rect = pos_texto.get_rect(topleft=(painel_x + 25, y_pos + 15))
        fundo_pos = criar_superficie_com_alpha((pos_rect.width + 4, pos_rect.height + 2), 120)
        fundo_pos.fill(CORES['AZUL_CLARO'])
        tela.blit(fundo_pos, (pos_rect.x - 2, pos_rect.y - 1))
        tela.blit(pos_texto, pos_rect)
        y_pos += 15
    
    # Ação do irrigador com fundo
    acao_texto = fonte_pequena.render(acao_irrigador, True, CORES['AZUL_ESCURO'])
    acao_rect = acao_texto.get_rect(topleft=(painel_x + 25, y_pos + 30))
    fundo_acao = criar_superficie_com_alpha((acao_rect.width + 4, acao_rect.height + 2), 100)
    fundo_acao.fill(CORES['AZUL_CLARO'])
    tela.blit(fundo_acao, (acao_rect.x - 2, acao_rect.y - 1))
    tela.blit(acao_texto, acao_rect)
    y_pos += 45

    # Colhedor com visual aprimorado
    colhedor_surface = criar_superficie_com_alpha((16, 16))
    desenhar_gradiente_circular(colhedor_surface, (8, 8), 8, CORES['AMARELO_DOURADO'], CORES['AMARELO_COLHEITA'])
    tela.blit(colhedor_surface, (painel_x + 5, y_pos + 3))
    
    tela.blit(fonte_pequena.render("Colhedor:", True, CORES['PRETO']),
              (painel_x + 25, y_pos))
    if pos_colhedor:
        pos_texto = fonte_pequena.render(f"Pos: {pos_colhedor}", True, CORES['AMARELO_ESCURO'])
        pos_rect = pos_texto.get_rect(topleft=(painel_x + 25, y_pos + 15))
        fundo_pos = criar_superficie_com_alpha((pos_rect.width + 4, pos_rect.height + 2), 120)
        fundo_pos.fill(CORES['AMARELO_DOURADO'])
        tela.blit(fundo_pos, (pos_rect.x - 2, pos_rect.y - 1))
        tela.blit(pos_texto, pos_rect)
        y_pos += 15
    
    # Ação do colhedor com fundo
    acao_texto = fonte_pequena.render(acao_colhedor, True, CORES['AMARELO_ESCURO'])
    acao_rect = acao_texto.get_rect(topleft=(painel_x + 25, y_pos + 30))
    fundo_acao = criar_superficie_com_alpha((acao_rect.width + 4, acao_rect.height + 2), 100)
    fundo_acao.fill(CORES['AMARELO_DOURADO'])
    tela.blit(fundo_acao, (acao_rect.x - 2, acao_rect.y - 1))
    tela.blit(acao_texto, acao_rect)
    y_pos += 45

    # Sensor com visual aprimorado
    sensor_surface = criar_superficie_com_alpha((16, 16))
    desenhar_gradiente_circular(sensor_surface, (8, 8), 8, CORES['CINZA_CLARO'], CORES['CINZA_MORTA'])
    tela.blit(sensor_surface, (painel_x + 5, y_pos + 3))
    
    tela.blit(fonte_pequena.render("Sensor:", True, CORES['PRETO']),
              (painel_x + 25, y_pos))
    
    # Leitura do sensor com fundo
    sensor_texto = fonte_pequena.render(leitura_sensor, True, CORES['PRETO'])
    sensor_rect = sensor_texto.get_rect(topleft=(painel_x + 25, y_pos + 30))
    fundo_sensor = criar_superficie_com_alpha((sensor_rect.width + 4, sensor_rect.height + 2), 100)
    fundo_sensor.fill(CORES['CINZA_CLARO'])
    tela.blit(fundo_sensor, (sensor_rect.x - 2, sensor_rect.y - 1))
    tela.blit(sensor_texto, sensor_rect)
    y_pos += 50

    # Linha separadora com gradiente
    for i in range(painel_w - 10):
        alpha = 200 - abs(i - (painel_w - 10) // 2) * 3
        alpha = max(0, min(255, int(alpha)))  # Ensure alpha is an integer between 0-255
        color = (CORES['PRETO'][0], CORES['PRETO'][1], CORES['PRETO'][2], alpha)  # Create RGBA tuple
        pygame.draw.line(tela, color, (painel_x + 5 + i, y_pos), (painel_x + 5 + i, y_pos + 1))
    y_pos += 15

    # MÉTRICAS com fundo destacado
    metricas_surface = criar_superficie_com_alpha((painel_w - 10, 25), 150)
    metricas_surface.fill(CORES['VERDE_LEGENDA'])
    tela.blit(metricas_surface, (painel_x + 5, y_pos - 5))
    
    tela.blit(fonte.render("MÉTRICAS", True, CORES['BRANCO']),
              (painel_x + 8, y_pos))
    y_pos += 30

    # Calcula plantas vivas
    largura_barra = painel_w - 30
    altura_barra = 18

    def draw_bar_melhorada(label, count, cor_inicio, cor_fim, y):
        # Texto da métrica
        texto_metrica = fonte_pequena.render(f"{label}: {count}", True, cor_fim)
        tela.blit(texto_metrica, (painel_x + 5, y))
        
        # Fundo da barra com gradiente sutil
        barra_rect = (painel_x + 5, y + 20, largura_barra, altura_barra)
        for i in range(altura_barra):
            ratio = i / altura_barra
            cor_fundo = [
                int(CORES['CINZA_CLARO'][j] * (1 - ratio) + CORES['CINZA_MORTA'][j] * ratio)
                for j in range(3)
            ]
            pygame.draw.line(tela, cor_fundo, (painel_x + 5, y + 20 + i), (painel_x + 5 + largura_barra, y + 20 + i))
        
        # Preenchimento da barra
        if total_plantas > 0:
            largura_preenchimento = min(int((count / total_plantas) * largura_barra), largura_barra)
            if largura_preenchimento > 0:
                desenhar_barra_gradiente(tela, (painel_x + 5, y + 20, largura_preenchimento, altura_barra),
                                       cor_inicio, cor_fim, 100)
        
        # Borda da barra
        pygame.draw.rect(tela, CORES['PRETO'], barra_rect, 2)
        
        # Efeito de brilho na barra
        if count > 0:
            brilho_surface = criar_superficie_com_alpha((largura_barra, 4), 60)
            brilho_surface.fill(CORES['BRANCO'])
            tela.blit(brilho_surface, (painel_x + 5, y + 22))

    # Desenha as barras melhoradas
    draw_bar_melhorada("Vivas", plantas_vivas, CORES['VERDE_JOVEM'], CORES['VERDE_SAUDAVEL'], y_pos)
    y_pos += 50
    draw_bar_melhorada("Colhidas", colhidas, CORES['AMARELO_DOURADO'], CORES['AMARELO_ESCURO'], y_pos)
    y_pos += 50
    draw_bar_melhorada("Mortas", mortas, CORES['LARANJA'], CORES['VERMELHO'], y_pos)
    y_pos += 50

    # Taxa de sucesso com visual aprimorado
    if (colhidas + mortas) > 0:
        taxa = (colhidas / (colhidas + mortas)) * 100
        if taxa > 70:
            cor_taxa = CORES['VERDE_SAUDAVEL']
            cor_fundo = CORES['VERDE_JOVEM']
        elif taxa > 40:
            cor_taxa = CORES['LARANJA']
            cor_fundo = CORES['AMARELO_DOURADO']
        else:
            cor_taxa = CORES['VERMELHO']
            cor_fundo = CORES['ROSA']
        
        taxa_texto = fonte_pequena.render(f"Taxa Sucesso: {taxa:.1f}%", True, cor_taxa)
        taxa_rect = taxa_texto.get_rect(topleft=(painel_x + 5, y_pos))
        fundo_taxa = criar_superficie_com_alpha((taxa_rect.width + 6, taxa_rect.height + 4), 120)
        fundo_taxa.fill(cor_fundo)
        tela.blit(fundo_taxa, (taxa_rect.x - 3, taxa_rect.y - 2))
        tela.blit(taxa_texto, taxa_rect)
        y_pos += 35

    # Tempo com visual aprimorado
    minutos, segundos = divmod(tempo_passado, 60)
    tempo_texto = fonte.render(f"Tempo: {minutos:02d}:{segundos:02d}", True, CORES['PRETO'])
    tempo_rect = tempo_texto.get_rect(topleft=(painel_x + 5, y_pos))
    
    # Fundo do tempo com gradiente
    fundo_tempo = criar_superficie_com_alpha((tempo_rect.width + 8, tempo_rect.height + 6), 150)
    for i in range(tempo_rect.width + 8):
        ratio = i / (tempo_rect.width + 8)
        cor_atual = [
            int(CORES['AZUL_CLARO'][j] * (1 - ratio) + CORES['AZUL_AGUA'][j] * ratio)
            for j in range(3)
        ]
        pygame.draw.line(fundo_tempo, cor_atual, (i, 0), (i, tempo_rect.height + 6))
    
    tela.blit(fundo_tempo, (tempo_rect.x - 4, tempo_rect.y - 3))
    pygame.draw.rect(tela, CORES['AZUL_ESCURO'], (tempo_rect.x - 4, tempo_rect.y - 3, tempo_rect.width + 8, tempo_rect.height + 6), 2)
    tela.blit(tempo_texto, tempo_rect)
    y_pos += 45

    # Linha separadora
    for i in range(painel_w - 10):
        alpha = 200 - abs(i - (painel_w - 10) // 2) * 3
        alpha = max(0, min(255, int(alpha)))  # Ensure alpha is an integer between 0-255
        color = (CORES['PRETO'][0], CORES['PRETO'][1], CORES['PRETO'][2], alpha)  # Create RGBA tuple
        pygame.draw.line(tela, color, (painel_x + 5 + i, y_pos), (painel_x + 5 + i, y_pos + 1))
    y_pos += 15

    # LEGENDA com fundo destacado
    legenda_surface = criar_superficie_com_alpha((painel_w - 10, 25), 150)
    legenda_surface.fill(CORES['PRETO'])
    tela.blit(legenda_surface, (painel_x + 5, y_pos - 5))
    
    tela.blit(fonte.render("LEGENDA", True, CORES['BRANCO']), (painel_x + 8, y_pos))
    y_pos += 25
    
    legendas = [
        ("Nível de Água", CORES['AZUL_AGUA']),
        ("Maturidade", CORES['VERDE_SAUDAVEL']),
        ("Baixa Água", CORES['VERMELHO']),
        ("Pronta Colheita", CORES['AMARELO_COLHEITA']),
        ("Posição Agentes", CORES['PRETO'])
    ]
    
    for texto, cor in legendas:
        # Indicador colorido com gradiente
        indicador_surface = criar_superficie_com_alpha((12, 12))
        desenhar_gradiente_circular(indicador_surface, (6, 6), 6, CORES['BRANCO'], cor)
        tela.blit(indicador_surface, (painel_x + 5, y_pos + 2))
        
        # Texto da legenda
        legenda_texto = fonte_pequena.render(texto, True, cor)
        tela.blit(legenda_texto, (painel_x + 22, y_pos))
        y_pos += 20

def desenhar_grid_fundo(tela, largura, altura, tamanho_grid=50):
    """Desenha uma grade sutil no fundo para melhor orientação visual"""
    tempo_atual = pygame.time.get_ticks()
    
    # Grid principal
    cor_grid_principal = (220, 220, 220)
    cor_grid_secundario = (240, 240, 240)
    
    # Linhas secundárias (mais finas)
    for x in range(0, largura, tamanho_grid // 2):
        alpha = 100 + 20 * math.sin(tempo_atual * 0.001 + x * 0.01)
        linha_surface = criar_superficie_com_alpha((1, altura), int(alpha))
        linha_surface.fill(cor_grid_secundario)
        tela.blit(linha_surface, (x, 0))
    
    for y in range(0, altura, tamanho_grid // 2):
        alpha = 100 + 20 * math.sin(tempo_atual * 0.001 + y * 0.01)
        linha_surface = criar_superficie_com_alpha((largura, 1), int(alpha))
        linha_surface.fill(cor_grid_secundario)
        tela.blit(linha_surface, (0, y))
    
    # Linhas principais (mais grossas)
    for x in range(0, largura, tamanho_grid):
        pygame.draw.line(tela, cor_grid_principal, (x, 0), (x, altura), 1)
    
    for y in range(0, altura, tamanho_grid):
        pygame.draw.line(tela, cor_grid_principal, (0, y), (largura, y), 1)

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
    
    # Fundo com gradiente
    fundo_w, fundo_h = 760, 50
    fundo_surface = criar_superficie_com_alpha((fundo_w, fundo_h), 200)
    
    # Gradiente horizontal
    for i in range(fundo_w):
        ratio = i / fundo_w
        cor_atual = [
            int(CORES['CINZA_CLARO'][j] * (1 - ratio) + CORES['BRANCO'][j] * ratio)
            for j in range(3)
        ]
        pygame.draw.line(fundo_surface, cor_atual, (i, 0), (i, fundo_h))
    
    tela.blit(fundo_surface, (x_offset, y_offset))
    
    # Borda decorativa
    pygame.draw.rect(tela, CORES['PRETO'], (x_offset, y_offset, fundo_w, fundo_h), 2)
    pygame.draw.line(tela, CORES['VERDE_LEGENDA'], (x_offset + 5, y_offset + 5), (x_offset + fundo_w - 5, y_offset + 5), 2)
    
    # Textos das estatísticas com fundos coloridos
    stats = [
        (f"Total: {total}", CORES['PRETO'], CORES['BRANCO']),
        (f"Vivas: {vivas}", CORES['VERDE_SAUDAVEL'], CORES['VERDE_JOVEM']),
        (f"Colhidas: {colhidas}", CORES['AMARELO_ESCURO'], CORES['AMARELO_DOURADO']),
        (f"Mortas: {mortas}", CORES['VERMELHO'], CORES['ROSA']),
        (f"Água: {agua_media:.1f}%", CORES['AZUL_ESCURO'], CORES['AZUL_CLARO']),
        (f"Maturidade: {maturidade_media:.1f}%", CORES['VERDE_MADURO'], CORES['VERDE_SAUDAVEL'])
    ]
    
    x_pos = x_offset + 15
    y_linha1 = y_offset + 12
    y_linha2 = y_offset + 30
    
    for i, (stat, cor_texto, cor_fundo) in enumerate(stats):
        y_atual = y_linha1 if i < 3 else y_linha2
        
        texto = fonte_pequena.render(stat, True, cor_texto)
        texto_rect = texto.get_rect(topleft=(x_pos, y_atual))
        
        # Fundo colorido
        fundo_stat = criar_superficie_com_alpha((texto_rect.width + 6, texto_rect.height + 4), 120)
        fundo_stat.fill(cor_fundo)
        tela.blit(fundo_stat, (texto_rect.x - 3, texto_rect.y - 2))
        
        # Borda
        pygame.draw.rect(tela, cor_texto, (texto_rect.x - 3, texto_rect.y - 2, texto_rect.width + 6, texto_rect.height + 4), 1)
        
        tela.blit(texto, texto_rect)
        x_pos += texto.get_width() + 25
        
        # Reset x_pos para segunda linha
        if i == 2:
            x_pos = x_offset + 15

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