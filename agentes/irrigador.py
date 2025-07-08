import time
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
import random
from abc import ABC, abstractmethod

AZUL = (70, 130, 180)

# ===== MÓDULO 1: SISTEMA FUZZY =====
class FuzzySet:
    """Representa um conjunto fuzzy com pontos de membership"""
    def __init__(self, name: str, points: List[Tuple[float, float]]):
        self.name = name
        self.points = points
    
    def membership(self, x: float) -> float:
        x_vals = [p[0] for p in self.points]
        y_vals = [p[1] for p in self.points]
        return np.interp(x, x_vals, y_vals)

class FuzzyVariable:
    """Variável fuzzy com múltiplos conjuntos"""
    def __init__(self, name: str, min_val: float, max_val: float):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.sets: Dict[str, FuzzySet] = {}
    
    def add_set(self, name: str, points: List[Tuple[float, float]]):
        self.sets[name] = FuzzySet(name, points)
    
    def fuzzify(self, value: float) -> Dict[str, float]:
        return {name: fset.membership(value) for name, fset in self.sets.items()}

# ===== MÓDULO 2: SISTEMA NEURO-FUZZY =====
class NeuroFuzzySystem:
    """Sistema neuro-fuzzy para inferência de irrigação"""
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
        
        self._init_rules()
    
    def _init_rules(self):
        self.rules = [
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
        """Inferência fuzzy para determinar necessidade de irrigação"""
        moisture_degrees = self.soil_moisture.fuzzify(soil_moisture)
        temp_degrees = self.temperature.fuzzify(temperature)
        
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
        
        return self._defuzzify(strengths, output_sets)
    
    def _defuzzify(self, strengths: List[float], output_sets: List[str]) -> float:
        """Defuzzificação usando método do centróide"""
        total_area = 0
        weighted_sum = 0
        
        centroid_map = {'pouco': 15, 'moderado': 50, 'muito': 85}
        
        for strength, out_set in zip(strengths, output_sets):
            if strength > 0:
                centroid = centroid_map[out_set]
                weighted_sum += strength * centroid
                total_area += strength
        
        return weighted_sum / total_area if total_area > 0 else 0
    
    def update_weights(self, error: float, learning_rate: float = None):
        """Atualiza pesos das regras baseado no erro"""
        lr = learning_rate or self.learning_rate
        for i in range(len(self.weights)):
            self.weights[i] -= lr * error
            self.weights[i] = max(0, min(1, self.weights[i]))

# ===== MÓDULO 3: DETECTOR DE NECESSIDADES =====
class NecessityDetector:
    """Detecta necessidades de irrigação das plantas"""
    def __init__(self, neuro_fuzzy: NeuroFuzzySystem, exploration_rate: float = 0.3):
        self.neuro_fuzzy = neuro_fuzzy
        self.exploration_rate = exploration_rate
        self.learning_history = []
        self.max_history_size = 100
    
    def detect_needs(self, plantas) -> Tuple[List, List]:
        """Classifica plantas em críticas e preventivas"""
        criticas = []
        preventivas = []
        
        for p in plantas:
            if p.coletada or p.morta:
                continue
            
            temperatura = getattr(p, 'temperatura', 25)
            necessidade = self.neuro_fuzzy.infer(p.agua, temperatura)
            
            # Exploração vs. explotação
            if random.random() < self.exploration_rate:
                necessidade = random.uniform(0, 100)
            
            if necessidade > 70:
                criticas.append((p, necessidade))
            elif necessidade > 30:
                preventivas.append((p, necessidade))
            
            self._add_to_learning_history({
                'umidade': p.agua,
                'temperatura': temperatura,
                'irrigacao': 0,
                'timestamp': time.time()
            })
        
        # Ordena por necessidade (maior primeiro)
        criticas = [p for p, _ in sorted(criticas, key=lambda x: -x[1])]
        preventivas = [p for p, _ in sorted(preventivas, key=lambda x: -x[1])]
        
        return criticas, preventivas
    
    def _add_to_learning_history(self, data):
        """Adiciona dados ao histórico de aprendizado"""
        self.learning_history.append(data)
        if len(self.learning_history) > self.max_history_size:
            self.learning_history.pop(0)
    
    def update_exploration_rate(self, decay_factor: float = 0.99):
        """Reduz a taxa de exploração ao longo do tempo"""
        self.exploration_rate = max(0.05, self.exploration_rate * decay_factor)

# ===== MÓDULO 4: ESTRATÉGIA DE DECISÃO =====
class DecisionStrategy(ABC):
    """Interface para estratégias de decisão"""
    @abstractmethod
    def decide(self, criticas: List, preventivas: List) -> Optional[Any]:
        pass

class CriticalFirstStrategy(DecisionStrategy):
    """Estratégia que prioriza plantas críticas"""
    def decide(self, criticas: List, preventivas: List) -> Optional[Any]:
        if criticas:
            return min(criticas, key=lambda p: p.agua)
        elif preventivas:
            return min(preventivas, key=lambda p: p.agua)
        return None

class BalancedStrategy(DecisionStrategy):
    """Estratégia balanceada entre críticas e preventivas"""
    def __init__(self, critical_weight: float = 0.7):
        self.critical_weight = critical_weight
    
    def decide(self, criticas: List, preventivas: List) -> Optional[Any]:
        # Pode implementar lógica mais complexa aqui
        if criticas and random.random() < self.critical_weight:
            return min(criticas, key=lambda p: p.agua)
        elif preventivas:
            return min(preventivas, key=lambda p: p.agua)
        elif criticas:
            return min(criticas, key=lambda p: p.agua)
        return None

# ===== MÓDULO 5: SISTEMA DE IRRIGAÇÃO =====
class IrrigationSystem:
    """Sistema responsável pela irrigação das plantas"""
    def __init__(self, neuro_fuzzy: NeuroFuzzySystem, base_water_amount: float = 70):
        self.neuro_fuzzy = neuro_fuzzy
        self.base_water_amount = base_water_amount
        self.historico = []
    
    def irrigate(self, planta) -> Tuple[Tuple[int, int], str]:
        """Irriga uma planta específica"""
        temperatura = getattr(planta, 'temperatura', 25)
        necessidade = self.neuro_fuzzy.infer(planta.agua, temperatura)
        
        agua_a_adicionar = min(
            (100 - planta.agua),
            necessidade * self.base_water_amount / 100.0
        )
        
        agua_original = planta.agua
        planta.agua = min(100, planta.agua + agua_a_adicionar)
        coords = (planta.x, planta.y)
        
        self.historico.append((
            time.time(),
            coords,
            agua_original,
            planta.agua,
            necessidade
        ))
        
        return coords, f"💧 Irrigou planta em {coords} (de {agua_original:.1f} para {planta.agua:.1f}, necessidade: {necessidade:.1f}%)"

# ===== MÓDULO 6: SISTEMA DE APRENDIZADO =====
class LearningSystem:
    """Sistema de aprendizado para o agente"""
    def __init__(self, neuro_fuzzy: NeuroFuzzySystem, necessity_detector: NecessityDetector):
        self.neuro_fuzzy = neuro_fuzzy
        self.necessity_detector = necessity_detector
    
    def update_from_feedback(self, umidade_anterior: float, umidade_atual: float, temperatura: float):
        """Atualiza o sistema com base no feedback"""
        if umidade_atual > umidade_anterior:
            error = (100 - umidade_atual) / 100.0
            self.neuro_fuzzy.update_weights(-error)
        
        self.necessity_detector.update_exploration_rate()

# ===== MÓDULO 7: AGENTE PRINCIPAL =====
class AgenteIrrigador:
    """Agente principal de irrigação modularizado"""
    def __init__(self, 
                 delay: float = 0.3,
                 learning_rate: float = 0.01,
                 base_water_amount: float = 70,
                 strategy: DecisionStrategy = None):
        
        self.delay = delay
        self.ultimo_tempo = 0
        self.contador_emergencia = 0
        
        # Inicializa módulos
        self.neuro_fuzzy = NeuroFuzzySystem(learning_rate)
        self.necessity_detector = NecessityDetector(self.neuro_fuzzy)
        self.irrigation_system = IrrigationSystem(self.neuro_fuzzy, base_water_amount)
        self.learning_system = LearningSystem(self.neuro_fuzzy, self.necessity_detector)
        
        # Estratégia de decisão
        self.strategy = strategy or CriticalFirstStrategy()
    
    def executar(self, plantas):
        """Executa o ciclo principal do agente"""
        agora = time.time()
        tempo_decorrido = agora - self.ultimo_tempo
        
        if tempo_decorrido < self.delay:
            return (0, 0), "⏳ Aguardando próximo ciclo..."
        
        # Detecta necessidades
        criticas, preventivas = self.necessity_detector.detect_needs(plantas)
        
        # Decide qual planta irrigar
        planta_alvo = self.strategy.decide(criticas, preventivas)
        
        if planta_alvo:
            if criticas and planta_alvo in criticas:
                self.contador_emergencia += 1
            
            # Irriga a planta
            agua_original = planta_alvo.agua
            coords, msg = self.irrigation_system.irrigate(planta_alvo)
            
            # Aprende com o feedback
            temperatura = getattr(planta_alvo, 'temperatura', 25)
            self.learning_system.update_from_feedback(agua_original, planta_alvo.agua, temperatura)
            
            self.ultimo_tempo = agora
            return coords, msg
        
        self.ultimo_tempo = agora
        return (0, 0), "✅ Nenhuma planta precisa de irrigação."
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de performance"""
        return {
            'total_irrigations': len(self.irrigation_system.historico),
            'emergency_count': self.contador_emergencia,
            'exploration_rate': self.necessity_detector.exploration_rate,
            'learning_history_size': len(self.necessity_detector.learning_history)
        }

# ===== FACTORY PARA CRIAÇÃO DE AGENTES =====
class AgentFactory:
    """Factory para criar diferentes tipos de agentes"""
    
    @staticmethod
    def create_basic_agent(delay: float = 0.3) -> AgenteIrrigador:
        """Cria um agente básico com estratégia crítica"""
        return AgenteIrrigador(delay=delay, strategy=CriticalFirstStrategy())
    
    @staticmethod
    def create_balanced_agent(delay: float = 0.3, critical_weight: float = 0.7) -> AgenteIrrigador:
        """Cria um agente balanceado"""
        strategy = BalancedStrategy(critical_weight)
        return AgenteIrrigador(delay=delay, strategy=strategy)
    
    @staticmethod
    def create_learning_agent(delay: float = 0.3, learning_rate: float = 0.05) -> AgenteIrrigador:
        """Cria um agente com aprendizado acelerado"""
        return AgenteIrrigador(delay=delay, learning_rate=learning_rate)

# ===== FUNÇÃO GLOBAL PARA COMPATIBILIDADE =====
agente_global = AgentFactory.create_basic_agent(delay=0.3)

def agir_irrigador(plantas):
    """Função global para manter compatibilidade"""
    return agente_global.executar(plantas)