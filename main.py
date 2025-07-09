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
relogio = pygame.time.Clock()

# Estado inicial
plantas = [Planta(80 + (i % 5) * 130, 80 + (i // 5) * 110) for i in range(20)]
TEMPO_INICIAL = time.time()

# Estados iniciais dos agentes
pos_irrigador = (0, 0)
pos_colhedor = (0, 0)
ultima_acao_irrigador = "Inicializando..."
ultima_acao_colhedor = "Inicializando..."
ultimas_leituras_sensor = "Coletando dados..."
irrigador_ativo = False
colhedor_ativo = False

# Estatísticas dos agentes
estatisticas_agentes = {
    'irrigador': {
        'plantas_regadas': 0,
        'agua_fornecida': 0,
        'ultima_acao': ""
    },
    'colhedor': {
        'plantas_colhidas': 0,
        'plantas_removidas': 0,
        'ultima_acao': ""
    },
    'sensor': {
        'leituras_realizadas': 0,
        'plantas_em_risco': 0,
        'ultima_leitura': ""
    }
}

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
        # Atualiza estatísticas do irrigador
        if "Irrigou" in acao_irrig:
            estatisticas_agentes['irrigador']['plantas_regadas'] += 1
            # Extrai a quantidade de água fornecida da mensagem
            try:
                agua = int(acao_irrig.split("para")[1].split(")")[0].strip())
                estatisticas_agentes['irrigador']['agua_fornecida'] += agua
            except:
                pass
    ultima_acao_irrigador = acao_irrig
    estatisticas_agentes['irrigador']['ultima_acao'] = acao_irrig
    irrigador_ativo = "Irrigando" in acao_irrig

    # Colhedor
    nova_pos_colh, acao_colh, colhida, morta = agir_colhedor(plantas, pos_colhedor)
    if tuple(nova_pos_colh) != (0, 0):
        pos_colhedor = tuple(nova_pos_colh)
        # Atualiza estatísticas do colhedor
        if colhida > 0:
            estatisticas_agentes['colhedor']['plantas_colhidas'] += colhida
        if morta > 0:
            estatisticas_agentes['colhedor']['plantas_removidas'] += morta
    
    ultima_acao_colhedor = acao_colh
    estatisticas_agentes['colhedor']['ultima_acao'] = acao_colh
    colhedor_ativo = "Colhendo" in acao_colh
    plantas_colhidas += colhida
    plantas_mortas += morta


    plantas_colhidas += colhida
    plantas_mortas += morta

    # Sensor
    leitura_anterior = ultimas_leituras_sensor
    resultado_sensor = agir_sensor(plantas)
    
    # Atualiza estatísticas do sensor
    if isinstance(resultado_sensor, dict):  # Nova leitura de dados
        estatisticas_agentes['sensor']['leituras_realizadas'] += 1
        estatisticas_agentes['sensor']['plantas_em_risco'] = len(resultado_sensor['plantas_criticas'])
        # Formata a mensagem para exibição no HUD
        if resultado_sensor['plantas_criticas']:
            crit_txt = f"Plantas com pouca água: {resultado_sensor['plantas_criticas'][:3]}"
            if len(resultado_sensor['plantas_criticas']) > 3:
                crit_txt += f" e mais {len(resultado_sensor['plantas_criticas']) - 3}..."
        else:
            crit_txt = "Todas as plantas estão hidratadas"
        
        ultimas_leituras_sensor = f"{crit_txt} | Água: {resultado_sensor['agua_media']:.1f}% | Maturidade: {resultado_sensor['maturidade_media']:.1f}%"
        estatisticas_agentes['sensor']['ultima_leitura'] = ultimas_leituras_sensor
    else:
        # Mantém a mensagem de espera
        ultimas_leituras_sensor = resultado_sensor

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
        plantas_colhidas, plantas_mortas, tempo_passado, len(plantas), plantas_vivas=sum(1 for p in plantas if not p.morta and not p.coletada)
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
        # Usa os dados do sensor se disponíveis, senão calcula
        if isinstance(ultimas_leituras_sensor, dict):
            vivas = ultimas_leituras_sensor['plantas_vivas']
            agua_media = ultimas_leituras_sensor['agua_media']
            maturidade_media = ultimas_leituras_sensor['maturidade_media']
        else:
            vivas = sum(1 for p in plantas if not p.morta and not p.coletada)
            if vivas > 0:
                agua_media = sum(p.agua for p in plantas if not p.morta and not p.coletada) / vivas
                maturidade_media = sum(p.maturidade for p in plantas if not p.morta and not p.coletada) / vivas
            else:
                agua_media = maturidade_media = 0
            print("\n" + "="*50)
            print(f"RELATÓRIO DE DESEMPENHO - {tempo_passado}s")
            print("="*50)
            
            # Relatório geral
            print("\n📊 VISÃO GERAL")
            print(f"🌱 Plantas vivas: {vivas}")
            print(f"💧 Nível médio de água: {agua_media:.1f}%")
            print(f"🌿 Maturidade média: {maturidade_media:.1f}%")
            
            # Relatório do Irrigador
            print("\n🚰 IRRIGADOR")
            print(f"💦 Plantas regadas: {estatisticas_agentes['irrigador']['plantas_regadas']}")
            print(f"💧 Água fornecida: {estatisticas_agentes['irrigador']['agua_fornecida']} unidades")
            print(f"⏱ Última ação: {estatisticas_agentes['irrigador']['ultima_acao']}")
            
            # Relatório do Colhedor
            print("\n🤖 COLHEDOR")
            print(f"🌾 Plantas colhidas: {estatisticas_agentes['colhedor']['plantas_colhidas']}")
            print(f"💀 Plantas removidas: {estatisticas_agentes['colhedor']['plantas_removidas']}")
            print(f"⏱ Última ação: {estatisticas_agentes['colhedor']['ultima_acao']}")
            
            # Relatório do Sensor
            print("\n📡 SENSOR")
            print(f"📊 Leituras realizadas: {estatisticas_agentes['sensor']['leituras_realizadas']}")
            print(f"⚠️ Plantas em risco: {estatisticas_agentes['sensor']['plantas_em_risco']}")
            print(f"⏱ Última leitura: {estatisticas_agentes['sensor']['ultima_leitura']}")
            
            print("\n" + "="*50 + "\n")
            
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
