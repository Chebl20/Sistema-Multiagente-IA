import time

AZUL = (70, 130, 180)

class AgenteIrrigador:
    def __init__(self, delay=0.3, limiar_critico=25, limiar_preventivo=45, quantidade_agua=70):
        self.ultimo_tempo = 0
        self.delay = delay
        self.limiar_critico = limiar_critico
        self.limiar_preventivo = limiar_preventivo
        self.quantidade_agua = quantidade_agua
        self.historico = []
        self.contador_emergencia = 0

    def detectar_necessidade(self, plantas):
        """Classifica plantas em críticas e preventivas com diferentes limiares"""
        criticas = []
        preventivas = []
        
        for p in plantas:
            if p.coletada or p.morta:
                continue
                
            if p.agua < self.limiar_critico:
                criticas.append(p)
            elif p.agua < self.limiar_preventivo:
                preventivas.append(p)
                
        return criticas, preventivas

    def decidir(self, criticas, preventivas):
        """Prioriza plantas críticas, depois preventivas pela urgência"""
        if criticas:
            self.contador_emergencia += 1
            return min(criticas, key=lambda p: p.agua)
        elif preventivas:
            return min(preventivas, key=lambda p: p.agua)
        return None

    def agir(self, planta):
        """Irrigação otimizada considerando o déficit até 100"""
        deficit = 100 - planta.agua
        agua_a_adicionar = min(deficit, self.quantidade_agua)
        agua_original = planta.agua
        
        planta.agua += agua_a_adicionar
        coords = (planta.x, planta.y)
        
        self.historico.append((
            time.time(), 
            coords,
            agua_original,
            planta.agua,
            self.contador_emergencia
        ))
        
        return coords, f"💧 Irrigou planta em {coords} (de {agua_original} para {planta.agua})"

    def executar(self, plantas):
        agora = time.time()
        tempo_decorrido = agora - self.ultimo_tempo
        
        if tempo_decorrido < self.delay:
            return (0, 0), "⏳ Aguardando próximo ciclo..."
        
        criticas, preventivas = self.detectar_necessidade(plantas)
        planta_alvo = self.decidir(criticas, preventivas)

        if planta_alvo:
            coords, msg = self.agir(planta_alvo)
            self.ultimo_tempo = agora
            return coords, msg
        
        self.ultimo_tempo = agora
        return (0, 0), "✅ Nenhuma planta precisa de irrigação."

# === Função global para importar fácil ===
agente_global = AgenteIrrigador(
    delay=0.3,
    limiar_critico=25,
    limiar_preventivo=45,
    quantidade_agua=70
)

def agir_irrigador(plantas):
    return agente_global.executar(plantas)