import time
CINZA = (169, 169, 169)

ultimo_tempo = 0
delay = 1.0  # segundos

def agir_sensor(plantas):
    global ultimo_tempo
    agora = time.time()
    if agora - ultimo_tempo < delay:
        return "Aguardando leitura..."

    info = [(i, round(p.maturidade, 1), round(p.agua, 1), p.coletada, p.morta)
            for i, p in enumerate(plantas)]
    criticas = [i for i, m, a, c, mto in info if a < 20 and not c and not mto]
    ultimo_tempo = agora
    return f"Plantas com pouca água: {criticas[:5]}"
 