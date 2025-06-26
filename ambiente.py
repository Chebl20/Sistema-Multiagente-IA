import random

class Planta:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.resetar()

    def resetar(self):
        self.maturidade = 0
        self.agua = 50
        self.coletada = False
        self.morta = False
        self.fator_crescimento = random.uniform(0.01, 0.7)
        self.fator_consumo = random.uniform(0.1, 0.9)
        self.tempo_madura_cheia = 0  # contador de tempo com maturidade 100%
        self.limite_tempo_madura_cheia = 10  # limite para morrer

    def atualizar(self):
        if self.morta or self.coletada:
            return
        
        if self.agua > 0:
            # Cresce maturidade
            self.maturidade = min(100, self.maturidade + self.fator_crescimento)
            self.agua = max(0, self.agua - self.fator_consumo)

            # Conta o tempo em que a planta está com maturidade 100%
            if self.maturidade >= 100:
                self.tempo_madura_cheia += 1
                if self.tempo_madura_cheia > self.limite_tempo_madura_cheia:
                    self.morta = True
            else:
                self.tempo_madura_cheia = 0  # reseta contador se não estiver 100%
        else:
            self.morta = True
