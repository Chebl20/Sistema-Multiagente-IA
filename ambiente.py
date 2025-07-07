import random

class Planta:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.resetar()

    def resetar(self):
        """Reinicia atributos da planta."""
        self.maturidade = random.uniform(0, 20)  # Começa variada
        self.agua = random.uniform(40, 70)       # Começa variada
        self.coletada = False
        self.morta = False
        self.fator_crescimento = random.uniform(0.2, 1.0)  # crescimento mais suave
        self.fator_consumo = random.uniform(0.3, 1.0)
        self.tempo_madura_cheia = 0
        self.limite_tempo_madura_cheia = random.randint(10, 20)  # limite aleatório

    def atualizar(self):
        """Atualiza estado da planta a cada ciclo."""
        if self.morta or self.coletada:
            return

        if self.agua > 0:
            # Crescimento
            self.maturidade = min(100, self.maturidade + self.fator_crescimento)
            # Consumo de água
            self.agua = max(0, self.agua - self.fator_consumo)

            if self.maturidade >= 100:
                self.tempo_madura_cheia += 1
                if self.tempo_madura_cheia > self.limite_tempo_madura_cheia:
                    self.morta = True
            else:
                self.tempo_madura_cheia = 0
        else:
            self.morta = True

    def esta_madura(self):
        """Retorna True se planta está pronta para colher."""
        return self.maturidade >= 100 and not self.morta and not self.coletada

    def esta_critica(self):
        """Retorna True se planta precisa urgentemente de água."""
        return self.agua < 20 and not self.morta and not self.coletada

    def status(self):
        """Retorna status textual resumido."""
        if self.morta:
            return "💀 Morta"
        if self.coletada:
            return "🌾 Colhida"
        if self.esta_madura():
            return "✅ Madura"
        if self.esta_critica():
            return "⚠️ Crítica"
        return "🌱 Saudável"

    def __str__(self):
        return f"Planta({self.x}, {self.y}) - Mat: {self.maturidade:.1f}%, Água: {self.agua:.1f}%, Status: {self.status()}"
