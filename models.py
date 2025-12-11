class Robo:
    def __init__(self, nome, cor, ataque, defesa, velocidade, personalidade):
        self.nome = nome
        self.cor = cor
        self.ataque = ataque
        self.defesa = defesa
        self.velocidade = velocidade
        self.personalidade = personalidade
        # HP vamos definir certinho na Fase 1

    def __repr__(self):
        return f"<Robo {self.nome} ({self.cor})>"
