import pygame
import time
from ambiente import Planta
from visual import (
    CORES,
    criar_fontes,
    desenhar_grid_fundo,
    desenhar_planta_melhorada,
    desenhar_agente_melhorado,
    desenhar_hud_melhorado,
    desenhar_estatisticas_tempo_real,
    obter_tempo_pygame,
)
from agentes.irrigador import agir_irrigador
from agentes.colhedor import agir_colhedor
from agentes.sensor import agir_sensor

# Inicialização do Pygame
pygame.init()
LARGURA, ALTURA = 1000, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sistema de Agricultura Automatizada - IA Competitiva")

# Fontes e tempo
fonte_principal, fonte_pequena = criar_fontes()
TEMPO_INICIAL = time.time()
relogio = pygame.time.Clock()

# Inicialização das plantas
plantas = [Planta(80 + (i % 5) * 130, 80 + (i // 5) * 110) for i in range(20)]

# Estados iniciais dos agentes
pos_irrigador = (0, 0)
pos_colhedor = (0, 0)
ultima_acao_irrigador = "Inicializando..."
ultima_acao_colhedor = "Inicializando..."
ultimas_leituras_sensor = "Coletando dados..."
irrigador_ativo = False
colhedor_ativo = False

# Contadores e controle de relatórios
plantas_colhidas = plantas_mortas = 0
plantas_colhidas_anterior = plantas_mortas_anterior = 0
ultimo_relatorio = -1

rodando = True

print("Sistema de Agricultura Automatizada Iniciado!")
print("Monitoramento visual melhorado ativo")
print("Agentes IA: Irrigador, Colhedor e Sensor")
print("-" * 50)

while rodando:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                print(f"Pausado - Tempo: {int(time.time() - TEMPO_INICIAL)}s")
                pygame.time.wait(1000)
            elif evento.key == pygame.K_r:
                # Reiniciar sistema
                plantas = [Planta(80 + (i % 5) * 130, 80 + (i // 5) * 110) for i in range(20)]
                plantas_colhidas = plantas_mortas = 0
                plantas_colhidas_anterior = plantas_mortas_anterior = 0
                ultima_acao_irrigador = ultima_acao_colhedor = "Inicializando..."
                ultimas_leituras_sensor = "Coletando dados..."
                ultimo_relatorio = -1
                print("Sistema reiniciado!")

    # Lógica de atualização
    tela.fill(CORES['BRANCO'])
    desenhar_grid_fundo(tela, 780, ALTURA)

    for planta in plantas:
        planta.atualizar()

    # Irrigador: só atualiza posição se tiver uma planta ativa
    nova_pos_irrig, acao_irrig = agir_irrigador(plantas)
    # ignora o (0,0) de idle — só move quando o irrigador realmente recebe uma planta
    if tuple(nova_pos_irrig) != (0, 0):
        pos_irrigador = tuple(nova_pos_irrig)
    ultima_acao_irrigador = acao_irrig
    irrigador_ativo = "Irrigando" in acao_irrig

    # Colhedor
    nova_pos_colh, acao_colh, colhida, morta = agir_colhedor(plantas, pos_colhedor)
    if tuple(nova_pos_colh) != (0, 0):
        pos_colhedor = tuple(nova_pos_colh)
    ultima_acao_colhedor = acao_colh
    colhedor_ativo = "Colhendo" in acao_colh
    plantas_colhidas += colhida
    plantas_mortas   += morta


    plantas_colhidas += colhida
    plantas_mortas += morta

    # Sensor
    ultimas_leituras_sensor = agir_sensor(plantas)

    # Tempo
    tempo_atual = obter_tempo_pygame()
    tempo_passado = int(time.time() - TEMPO_INICIAL)

    # Renderização
    for planta in plantas:
        desenhar_planta_melhorada(tela, planta, fonte_pequena, tempo_atual)

    desenhar_agente_melhorado(tela, pos_irrigador, "irrigador", irrigador_ativo, fonte_pequena)
    desenhar_agente_melhorado(tela, pos_colhedor, "colhedor", colhedor_ativo, fonte_pequena)

    desenhar_hud_melhorado(
        tela, fonte_principal, fonte_pequena,
        ultima_acao_irrigador, ultima_acao_colhedor, ultimas_leituras_sensor,
        plantas_colhidas, plantas_mortas, tempo_passado, len(plantas)
    )

    desenhar_estatisticas_tempo_real(tela, fonte_pequena, plantas)

    # Feedback para colheitas e mortes únicas
    if plantas_colhidas != plantas_colhidas_anterior:
        print(f"Planta colhida! Total: {plantas_colhidas}")
        plantas_colhidas_anterior = plantas_colhidas
    if plantas_mortas != plantas_mortas_anterior:
        print(f"Planta morreu! Total: {plantas_mortas}")
        plantas_mortas_anterior = plantas_mortas

    # Relatório periódico a cada 30s (apenas uma vez)
    if tempo_passado % 30 == 0 and tempo_passado != ultimo_relatorio and tempo_passado > 0:
        vivas = sum(1 for p in plantas if not p.morta and not p.coletada)
        if vivas > 0:
            agua_media = sum(p.agua for p in plantas if not p.morta and not p.coletada) / vivas
            maturidade_media = sum(p.maturidade for p in plantas if not p.morta and not p.coletada) / vivas
            print(f"Relatório {tempo_passado}s - Vivas: {vivas}, Água: {agua_media:.1f}%, Maturidade: {maturidade_media:.1f}%")
        ultimo_relatorio = tempo_passado

    pygame.display.flip()
    relogio.tick(12)

# Relatório final
print("\n" + "="*50)
print("RELATÓRIO FINAL DO SISTEMA")
print("="*50)
print(f"Tempo total de execução: {tempo_passado} segundos")
print(f"Total de plantas: {len(plantas)}")
print(f"Plantas colhidas: {plantas_colhidas}")
print(f"Plantas mortas: {plantas_mortas}")
vivas_final = sum(1 for p in plantas if not p.morta and not p.coletada)
print(f"Plantas ainda vivas: {vivas_final}")

if plantas_colhidas + plantas_mortas > 0:
    taxa_sucesso = plantas_colhidas / (plantas_colhidas + plantas_mortas) * 100
    print(f"Taxa de sucesso: {taxa_sucesso:.1f}%")
    if taxa_sucesso >= 80:
        print("EXCELENTE! Sistema altamente eficiente!")
    elif taxa_sucesso >= 60:
        print("BOM! Sistema funcionando adequadamente")
    elif taxa_sucesso >= 40:
        print("REGULAR. Sistema precisa de ajustes")
    else:
        print("CRÍTICO! Sistema requer revisão urgente")
print("=" * 50)

pygame.quit()
