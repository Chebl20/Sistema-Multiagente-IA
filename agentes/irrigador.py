import time
AZUL = (70, 130, 180)

# Estado interno do agente
ultimo_tempo = 0
delay = 1.5  # segundos

def agir_irrigador(plantas):
    global ultimo_tempo
    agora = time.time()
    if agora - ultimo_tempo < delay:
        return (0, 0), "Aguardando próximo ciclo..."
    
    for planta in plantas:
        if planta.agua < 30 and not planta.coletada and not planta.morta:
            planta.agua += 20
            ultimo_tempo = agora
            return (planta.x, planta.y), f"Irrigou planta em ({planta.x}, {planta.y})"
    
    ultimo_tempo = agora
    return (0, 0), "Nenhuma planta irrigada"
