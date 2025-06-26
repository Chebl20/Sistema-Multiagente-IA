import time
AMARELO = (255, 215, 0)

ultimo_tempo = 0
delay = 2.0  # segundos

def agir_colhedor(plantas):
    global ultimo_tempo
    agora = time.time()
    if agora - ultimo_tempo < delay:
        return (0, 0), "Aguardando próximo ciclo...", 0, 0

    for planta in plantas:
        if planta.maturidade >= 100 and not planta.coletada and not planta.morta:
            planta.coletada = True
            pos = (planta.x, planta.y)
            planta.resetar()
            ultimo_tempo = agora
            return pos, f"Colheu e replantou em ({planta.x}, {planta.y})", 1, 0
        elif planta.morta and not planta.coletada:
            planta.coletada = True
            pos = (planta.x, planta.y)
            planta.resetar()
            ultimo_tempo = agora
            return pos, f"Removeu planta morta em ({planta.x}, {planta.y})", 0, 1

    ultimo_tempo = agora
    return (0, 0), "Nenhuma ação feita", 0, 0
    