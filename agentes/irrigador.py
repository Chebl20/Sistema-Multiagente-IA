import time
import numpy as np
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
import random

AZUL = (70, 130, 180)

class FuzzySet:
    def __init__(self, name: str, points: List[Tuple[float, float]]):
        self.name = name
        self.points = points
    
    def membership(self, x: float) -> float:
        x_vals = [p[0] for p in self.points]
        y_vals = [p[1] for p in self.points]
        return np.interp(x, x_vals, y_vals)

class FuzzyVariable:
    def __init__(self, name: str, min_val: float, max_val: float):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.sets: Dict[str, FuzzySet] = {}
    
    def add_set(self, name: str, points: List[Tuple[float, float]]):
        self.sets[name] = FuzzySet(name, points)
    
    def fuzzify(self, value: float) -> Dict[str, float]:
        return {name: fset.membership(value) for name, fset in self.sets.items()}

class NeuroFuzzySystem:
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate
        self.rules = []
        self.weights = []
        self._init_variables()
    
    def _init_variables(self):
        # Variáveis de entrada
        self.soil_moisture = FuzzyVariable('soil_moisture', 0, 100)
        self.soil_moisture.add_set('seco', [(0, 1), (30, 0)])
        self.soil_moisture.add_set('ideal', [(20, 0), (50, 1), (80, 0)])
        self.soil_moisture.add_set('umido', [(70, 0), (100, 1)])
        
        self.temperature = FuzzyVariable('temperature', 0, 50)
        self.temperature.add_set('frio', [(0, 1), (20, 0)])
        self.temperature.add_set('agradavel', [(15, 0), (25, 1), (35, 0)])
        self.temperature.add_set('quente', [(30, 0), (50, 1)])
        
        # Variável de saída
        self.irrigation = FuzzyVariable('irrigation', 0, 100)
        self.irrigation.add_set('pouco', [(0, 1), (30, 0)])
        self.irrigation.add_set('moderado', [(20, 0), (50, 1), (80, 0)])
        self.irrigation.add_set('muito', [(70, 0), (100, 1)])
        
        # Inicializa regras fuzzy
        self._init_rules()
    
    def _init_rules(self):
        # Regras baseadas em conhecimento de domínio
        self.rules = [
            # (input1_set, input2_set, output_set)
            ('seco', 'quente', 'muito'),
            ('seco', 'agradavel', 'muito'),
            ('seco', 'frio', 'moderado'),
            ('ideal', 'quente', 'moderado'),
            ('ideal', 'agradavel', 'pouco'),
            ('ideal', 'frio', 'pouco'),
            ('umido', 'quente', 'pouco'),
            ('umido', 'agradavel', 'pouco'),
            ('umido', 'frio', 'pouco'),
        ]
        self.weights = [1.0] * len(self.rules)
    
    def infer(self, soil_moisture: float, temperature: float) -> float:
        # Fuzzificação
        moisture_degrees = self.soil_moisture.fuzzify(soil_moisture)
        temp_degrees = self.temperature.fuzzify(temperature)
        
        # Aplicação das regras
        strengths = []
        output_sets = []
        
        for i, rule in enumerate(self.rules):
            moist_set, temp_set, out_set = rule
            strength = min(
                moisture_degrees.get(moist_set, 0),
                temp_degrees.get(temp_set, 0)
            ) * self.weights[i]
            strengths.append(strength)
            output_sets.append(out_set)
        
        # Defuzzificação (método do centróide)
        total_area = 0
        weighted_sum = 0
        
        for strength, out_set in zip(strengths, output_sets):
            if strength > 0:
                # Simplificação: usando o ponto médio do conjunto fuzzy de saída
                if out_set == 'pouco':
                    centroid = 15
                elif out_set == 'moderado':
                    centroid = 50
                else:  # muito
                    centroid = 85
                
                weighted_sum += strength * centroid
                total_area += strength
        
        if total_area == 0:
            return 0
            
        return weighted_sum / total_area
    
    def update_weights(self, error: float, learning_rate: float = None):
        """Atualiza os pesos das regras com base no erro"""
        lr = learning_rate or self.learning_rate
        for i in range(len(self.weights)):
            # Atualização simples baseada no gradiente descendente
            self.weights[i] -= lr * error
            # Garante que os pesos fiquem entre 0 e 1
            self.weights[i] = max(0, min(1, self.weights[i]))

class AgenteIrrigador:
    def __init__(self, delay=0.3, limiar_critico=25, limiar_preventivo=45, quantidade_agua=70):
        self.ultimo_tempo = 0
        self.delay = delay
        self.limiar_critico = limiar_critico
        self.limiar_preventivo = limiar_preventivo
        self.quantidade_agua = quantidade_agua
        self.historico = []
        self.contador_emergencia = 0
        
        # Inicializa o sistema neuro-fuzzy
        self.neuro_fuzzy = NeuroFuzzySystem(learning_rate=0.01)
        
        # Histórico para aprendizado
        self.learning_history = []
        self.max_history_size = 100
        
        # Fator de exploração (para balancear exploração vs. explotação)
        self.exploration_rate = 0.3

    def detectar_necessidade(self, plantas):
        """Classifica plantas em críticas e preventivas usando lógica fuzzy"""
        criticas = []
        preventivas = []
        
        for p in plantas:
            if p.coletada or p.morta:
                continue
                
            # Usa o sistema neuro-fuzzy para avaliar a necessidade de irrigação
            # Considera a umidade do solo e a temperatura como entradas
            temperatura = getattr(p, 'temperatura', 25)  # Valor padrão se não houver temperatura
            necessidade = self.neuro_fuzzy.infer(p.agua, temperatura)
            
            # Aplica um fator de exploração para tentar novas ações
            if random.random() < self.exploration_rate:
                necessidade = random.uniform(0, 100)
            
            # Classificação baseada na saída do neuro-fuzzy
            if necessidade > 70:
                criticas.append((p, necessidade))
            elif necessidade > 30:
                preventivas.append((p, necessidade))
            
            # Armazena para aprendizado posterior
            self._add_to_learning_history({
                'umidade': p.agua,
                'temperatura': temperatura,
                'irrigacao': 0,  # Será atualizado quando a planta for irrigada
                'timestamp': time.time()
            })
        
        # Ordena por necessidade (maior primeiro)
        criticas = [p for p, _ in sorted(criticas, key=lambda x: -x[1])]
        preventivas = [p for p, _ in sorted(preventivas, key=lambda x: -x[1])]
                
        return criticas, preventivas

    def decidir(self, criticas, preventivas):
        """Prioriza plantas críticas, depois preventivas pela urgência"""
        if criticas:
            self.contador_emergencia += 1
            return min(criticas, key=lambda p: p.agua)
        elif preventivas:
            return min(preventivas, key=lambda p: p.agua)
        return None

    def _add_to_learning_history(self, data):
        """Adiciona dados ao histórico de aprendizado"""
        self.learning_history.append(data)
        if len(self.learning_history) > self.max_history_size:
            self.learning_history.pop(0)
    
    def _update_learning(self, umidade_anterior, umidade_atual, temperatura):
        """Atualiza os pesos do sistema neuro-fuzzy com base no feedback"""
        if umidade_atual > umidade_anterior:
            # A irrigação foi bem-sucedida (aumentou a umidade)
            # Calcula o erro (quanto mais próximo de 100, melhor)
            error = (100 - umidade_atual) / 100.0
            self.neuro_fuzzy.update_weights(-error)  # Queremos minimizar o erro
        
        # Reduz a taxa de exploração ao longo do tempo
        self.exploration_rate = max(0.05, self.exploration_rate * 0.99)
    
    def agir(self, planta):
        """Irrigação otimizada usando o sistema neuro-fuzzy"""
        # Calcula a quantidade de água baseada no sistema neuro-fuzzy
        temperatura = getattr(planta, 'temperatura', 25)
        necessidade = self.neuro_fuzzy.infer(planta.agua, temperatura)
        
        # Aplica a quantidade de água proporcional à necessidade
        agua_a_adicionar = min(
            (100 - planta.agua),  # Não ultrapassar 100
            necessidade * self.quantidade_agua / 100.0  # Escala proporcional
        )
        
        agua_original = planta.agua
        planta.agua = min(100, planta.agua + agua_a_adicionar)
        coords = (planta.x, planta.y)
        
        # Registra a ação
        self.historico.append((
            time.time(), 
            coords,
            agua_original,
            planta.agua,
            self.contador_emergencia,
            necessidade
        ))
        
        # Atualiza o histórico de aprendizado com o feedback
        self._update_learning(agua_original, planta.agua, temperatura)
        
        return coords, f"💧 Irrigou planta em {coords} (de {agua_original:.1f} para {planta.agua:.1f}, necessidade: {necessidade:.1f}%)"
    
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