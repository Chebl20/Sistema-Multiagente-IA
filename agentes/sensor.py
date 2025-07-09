import time

# Cores
CINZA = (169, 169, 169)

# Variáveis globais que armazenarão o estado atual das plantas
plantas_criticas = []
plantas_preventivas = []
plantas_maduras = []
plantas_mortas = []

ultimo_tempo = 0
delay = 1.0  # segundos

def agir_sensor(plantas):
    global ultimo_tempo
    global plantas_criticas, plantas_preventivas, plantas_maduras, plantas_mortas

    agora = time.time()
    if agora - ultimo_tempo < delay:
        return "Aguardando leitura..."

    # Limpa listas anteriores
    plantas_criticas = []
    plantas_preventivas = []
    plantas_maduras = []
    plantas_mortas = []

    for p in plantas:
        if not p.coletada:
            if p.agua < 25:
                plantas_criticas.append(p)
            elif p.agua < 45:
                plantas_preventivas.append(p)

            if p.maturidade >= 100 and not p.morta:
                plantas_maduras.append(p)
            if p.morta:
                plantas_mortas.append(p)

    ultimo_tempo = agora

    return f"Irrigação → Críticas: {len(plantas_criticas)}, Preventivas: {len(plantas_preventivas)} | " \
           f"Colheita → Maduras: {len(plantas_maduras)}, Mortas: {len(plantas_mortas)}"
