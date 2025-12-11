import random

class Arena:
    def __init__(self, largura=16, altura=5):
        """
        Arena lógica em forma de grade.
        Por enquanto é retangular, depois podemos pensar em hexágono visual.
        """
        self.largura = largura
        self.altura = altura

    def distancia(self, robo1, robo2):
        """Distância Manhattan entre dois robôs."""
        return abs(robo1.x - robo2.x) + abs(robo1.y - robo2.y)

    def limitar_posicao(self, x, y):
        """Garante que o robô não saia da arena."""
        x = max(0, min(self.largura - 1, x))
        y = max(0, min(self.altura - 1, y))
        return x, y


class Robo:
    def __init__(self, nome, cor, ataque, defesa, velocidade, personalidade):
        self.nome = nome
        self.cor = cor
        self.ataque = ataque
        self.defesa = defesa
        self.velocidade = velocidade
        self.personalidade = personalidade

        # HP máximo = defesa * 10 (regra simples para começar)
        self.hp_max = defesa * 10
        self.hp_atual = self.hp_max

        # Preferências de comportamento (ajustadas pelos comandos do jogador)
        self.pref_ataque = 1
        self.pref_defesa = 1
        self.pref_esquiva = 1

        # Posição na arena (x, y)
        self.x = 0
        self.y = 0

    # -----------------------------------------
    # Posição / movimento
    # -----------------------------------------

    def set_posicao(self, x, y, arena: Arena | None = None):
        """Define a posição inicial do robô."""
        if arena is not None:
            x, y = arena.limitar_posicao(x, y)
        self.x = x
        self.y = y

    def posicao(self):
        return self.x, self.y

    def mover_em_direcao(self, alvo: "Robo", arena: Arena, aproximar=True):
        """
        Move um passo em direção (aproximar=True) ou afastando (aproximar=False) do alvo.
        Por enquanto, sempre 1 passo por turno.
        """
        dx = 0
        dy = 0

        if alvo.x > self.x:
            dx = 1
        elif alvo.x < self.x:
            dx = -1

        if alvo.y > self.y:
            dy = 1
        elif alvo.y < self.y:
            dy = -1

        if not aproximar:
            dx = -dx
            dy = -dy

        novo_x = self.x + dx
        novo_y = self.y + dy
        novo_x, novo_y = arena.limitar_posicao(novo_x, novo_y)

        self.x = novo_x
        self.y = novo_y

    # -----------------------------------------
    # Lógica de combate
    # -----------------------------------------

    def receber_dano(self, valor):
        dano_final = max(1, valor - self.defesa)
        self.hp_atual -= dano_final
        return dano_final

    def atacar(self, alvo):
        dano_base = self.ataque + random.randint(0, 2)
        return alvo.receber_dano(dano_base)

    def esta_vivo(self):
        return self.hp_atual > 0

    # -----------------------------------------
    # Preferências do jogador (comandos)
    # -----------------------------------------

    def aplicar_preferencias(self, preferencias: dict):
        """
        Atualiza as preferências de comportamento do robô
        com base no dicionário gerado pelo interpretar_comando.
        Ex: {"ataque": +2, "defesa": -1}
        """

        self.pref_ataque = max(1, self.pref_ataque + preferencias.get("ataque", 0))
        self.pref_defesa = max(1, self.pref_defesa + preferencias.get("defesa", 0))
        self.pref_esquiva = max(1, self.pref_esquiva + preferencias.get("esquiva", 0))

    # -----------------------------------------
    # Lógica da IA do robô (usando personalidade + prefs)
    # -----------------------------------------

    def escolher_acao(self):
        """
        IA simples:
        - Personalidade define a base
        - Preferências (comando do jogador) ajustam os pesos
        """

        # Base pela personalidade
        if self.personalidade == "agressivo":
            base = {"atacar": 3, "defender": 1, "esquivar": 1}
        elif self.personalidade == "defensivo":
            base = {"atacar": 1, "defender": 3, "esquivar": 2}
        elif self.personalidade == "velocista":
            base = {"atacar": 2, "defender": 1, "esquivar": 3}
        else:
            base = {"atacar": 1, "defender": 1, "esquivar": 1}

        # Ajuste pelas preferências
        pesos = {
            "atacar": base["atacar"] * self.pref_ataque,
            "defender": base["defender"] * self.pref_defesa,
            "esquivar": base["esquivar"] * self.pref_esquiva,
        }

        acoes = list(pesos.keys())
        valores = list(pesos.values())

        acao_escolhida = random.choices(acoes, weights=valores, k=1)[0]
        return acao_escolhida
