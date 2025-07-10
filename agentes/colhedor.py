### colhedor.py
import time

AMARELO = (255, 215, 0)

ultimo_tempo = 0
delay = 0.0  # segundos

def agir_colhedor(plantas, pos_atual):
    global ultimo_tempo

    agora = time.time()
    if agora - ultimo_tempo < delay:
        return pos_atual, "Aguardando próximo ciclo...", 0, 0

    pendentes = [p for p in plantas if not p.coletada]
    maduros = [p for p in pendentes if (not p.morta) and p.maturidade >= 100]
    mortos  = [p for p in pendentes if p.morta]

    def dist2(p):
        dx = p.x - pos_atual[0]
        dy = p.y - pos_atual[1]
        return dx*dx + dy*dy

    if maduros:
        alvo = min(maduros, key=dist2)
        acao = "colher"
    elif mortos:
        alvo = min(mortos, key=dist2)
        acao = "remover"
    else:
        ultimo_tempo = agora
        return pos_atual, "Nenhuma ação possível", 0, 0

    alvo.coletada = True
    coords = (alvo.x, alvo.y)
    alvo.resetar()
    ultimo_tempo = agora

    if acao == "colher":
        return coords, f"Colheu e replantou em {coords}", 1, 0
    else:
        return coords, f"Removeu planta morta em {coords}", 0, 1
