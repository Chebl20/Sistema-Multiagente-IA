import time
from typing import List, Tuple

AMARELO = (255, 215, 0)

class AgenteColhedor:
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self._ultimo_tempo = 0.0

    def agir(self, plantas: List, pos_atual: Tuple[int, int]) -> Tuple[Tuple[int, int], str, int, int]:
        """
        Executa ação de coleta ou remoção em plantas próximas.

        :param plantas: lista de objetos com atributos x, y, maturidade, morta, coletada, e método resetar()
        :param pos_atual: tupla (x, y) da posição atual do agente
        :return: nova posição, mensagem, total colhido, total removido
        """
        agora = time.time()
        if agora - self._ultimo_tempo < self.delay:
            return pos_atual, "Aguardando próximo ciclo...", 0, 0

        pendentes = [p for p in plantas if not p.coletada]
        maduros = [p for p in pendentes if not p.morta and p.maturidade >= 100]
        mortos  = [p for p in pendentes if p.morta]

        def dist2(p):
            dx = p.x - pos_atual[0]
            dy = p.y - pos_atual[1]
            return dx * dx + dy * dy

        if maduros:
            alvo = min(maduros, key=dist2)
            acao = "colher"
        elif mortos:
            alvo = min(mortos, key=dist2)
            acao = "remover"
        else:
            self._ultimo_tempo = agora
            return pos_atual, "Nenhuma planta disponível para ação", 0, 0

        coords = (alvo.x, alvo.y)
        alvo.coletada = True
        alvo.resetar()
        self._ultimo_tempo = agora

        if acao == "colher":
            return coords, f"✅ Colheu e replantou planta em {coords}", 1, 0
        else:
            return coords, f"🪦 Removeu planta morta em {coords}", 0, 1

colhedor = AgenteColhedor()

def agir_colhedor(plantas, pos_colhedor):
    return colhedor.agir(plantas, pos_colhedor)
