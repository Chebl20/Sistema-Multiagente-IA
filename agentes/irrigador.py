import time  # Para controlar o intervalo entre ações

AZUL = (70, 130, 180)  # Cor do agente irrigador (visual)

class AgenteIrrigador:
    def __init__(self, delay=0.3, limiar_critico=25, limiar_preventivo=45, quantidade_agua=70):
        self.ultimo_tempo = 0  # Última irrigação
        self.delay = delay  # Intervalo entre ações
        self.limiar_critico = limiar_critico  # Água mínima crítica
        self.limiar_preventivo = limiar_preventivo  # Água mínima preventiva
        self.quantidade_agua = quantidade_agua  # Quanto irrigar por vez
        self.historico = []  # Registro de ações
        self.contador_emergencia = 0  # Quantas vezes agiu em emergência

    def decidir(self, criticas, preventivas):
        if criticas:
            self.contador_emergencia += 1
            return min(criticas, key=lambda p: p.agua)
        elif preventivas:
            return min(preventivas, key=lambda p: p.agua)
        return None

    def agir(self, planta):
        deficit = 100 - planta.agua
        agua_a_adicionar = min(deficit, self.quantidade_agua)
        agua_original = planta.agua
        planta.agua += agua_a_adicionar
        coords = (planta.x, planta.y)

        self.historico.append((
            time.time(), coords, agua_original, planta.agua, self.contador_emergencia
        ))

        return coords, f"💧 Irrigou planta em {coords} (de {agua_original} para {planta.agua})"

    def executar(self, plantas):
        agora = time.time()
        if agora - self.ultimo_tempo < self.delay:
            return (0, 0), "⏳ Aguardando próximo ciclo..."

        criticas = [p for p in plantas if p.agua < self.limiar_critico]
        preventivas = [p for p in plantas if self.limiar_critico <= p.agua < self.limiar_preventivo]
        planta_alvo = self.decidir(criticas, preventivas)

        if planta_alvo:
            coords, msg = self.agir(planta_alvo)
            self.ultimo_tempo = agora
            return coords, msg

        self.ultimo_tempo = agora
        return (0, 0), "✅ Nenhuma planta precisa de irrigação."

# Instância global usada no sistema
agente_global = AgenteIrrigador()

# Função externa chamada pelo sistema principal
def agir_irrigador(plantas):
    return agente_global.executar(plantas)
