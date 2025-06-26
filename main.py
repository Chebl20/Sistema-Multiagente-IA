import pygame
import time
from ambiente import Planta
from visual import *
from agentes.irrigador import agir_irrigador
from agentes.colhedor import agir_colhedor
from agentes.sensor import agir_sensor

pygame.init()
LARGURA, ALTURA = 1000, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Agricultura Automatizada")
fonte = pygame.font.SysFont("arial", 16)
TEMPO_INICIAL = time.time()

plantas = [Planta(100 + (i % 5) * 120, 100 + (i // 5) * 100) for i in range(20)]
pos_irrigador = [0, 0]
pos_colhedor = [0, 0]
ultima_acao_irrigador = ""
ultima_acao_colhedor = ""
ultimas_leituras_sensor = ""

relogio = pygame.time.Clock()
rodando = True

# contadores
plantas_colhidas = 0
plantas_mortas = 0

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((255, 255, 255))

    for planta in plantas:
        planta.atualizar()

    # Ações dos agentes
    pos_irrigador, ultima_acao_irrigador = agir_irrigador(plantas)
    pos_colhedor, acao_colhedor, nova_colhida, nova_morta = agir_colhedor(plantas)
    ultima_acao_colhedor = acao_colhedor
    plantas_colhidas += nova_colhida
    plantas_mortas += nova_morta
    ultimas_leituras_sensor = agir_sensor(plantas)

    for planta in plantas:
        desenhar_planta(tela, planta, fonte)
    desenhar_irrigador(tela, pos_irrigador)
    desenhar_colhedor(tela, pos_colhedor)

    tempo_passado = int(time.time() - TEMPO_INICIAL)
    desenhar_hud(tela, fonte, ultima_acao_irrigador, ultima_acao_colhedor,
                 ultimas_leituras_sensor, plantas_colhidas, plantas_mortas, tempo_passado)

    pygame.display.flip()
    relogio.tick(10)

pygame.quit()
