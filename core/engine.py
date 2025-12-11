from __future__ import annotations

import random
from typing import List, Literal, Optional

from .models import Robo, Arena


StatusJogo = Literal["running", "player_won", "enemy_won"]


def interpretar_comando(texto: str) -> dict:
    """
    Mesma lógica de antes, mas agora pensada para uso pela API.
    Converte o texto em ajustes de preferência.
    """
    texto = texto.lower()
    preferencias = {"ataque": 0, "defesa": 0, "esquiva": 0}

    if not texto.strip():
        return preferencias

    if "ataq" in texto or "agress" in texto or "bate" in texto:
        preferencias["ataque"] += 2

    if "defes" in texto or "proteg" in texto or "tank" in texto:
        preferencias["defesa"] += 2

    if "esquiv" in texto or "desvi" in texto or "foge" in texto or "distân" in texto:
        preferencias["esquiva"] += 2

    if "contra" in texto:
        preferencias["defesa"] += 1
        preferencias["ataque"] += 1

    return preferencias


class GameState:
    """
    Representa o estado de UMA luta:
    - arena
    - robo do jogador
    - robo adversário
    - turno atual
    - status (running / player_won / enemy_won)
    - logs das ações (pra mostrar no front)
    """

    def __init__(self, jogador: Robo, adversario: Robo, arena: Arena):
        self.arena = arena
        self.jogador = jogador
        self.adversario = adversario
        self.turno = 1
        self.status: StatusJogo = "running"
        self.logs: List[str] = []

        # posição inicial
        self.jogador.set_posicao(2, 1, arena)
        self.adversario.set_posicao(arena.largura - 3, arena.altura - 2, arena)

        self.logs.append(
            f"Iniciando batalha: {self.jogador.nome} vs {self.adversario.nome}."
        )

    # -------------------------------
    # Comandos do jogador
    # -------------------------------

    def aplicar_comando(self, texto: str):
        prefs = interpretar_comando(texto)
        self.jogador.aplicar_preferencias(prefs)
        self.logs.append(
            f"Comando recebido: '{texto}'. "
            f"Prefs -> ATAQUE x{self.jogador.pref_ataque}, "
            f"DEFESA x{self.jogador.pref_defesa}, "
            f"ESQUIVA x{self.jogador.pref_esquiva}."
        )

    # -------------------------------
    # Execução de 1 turno
    # -------------------------------

    def executar_turno(self):
        if self.status != "running":
            self.logs.append("O jogo já terminou. Nenhum turno executado.")
            return

        self.logs.append(f"--- TURNO {self.turno} ---")

        ordem = sorted(
            [self.jogador, self.adversario],
            key=lambda r: r.velocidade,
            reverse=True,
        )

        for robo in ordem:
            if not self.jogador.esta_vivo() or not self.adversario.esta_vivo():
                break

            alvo = self.adversario if robo is self.jogador else self.jogador
            dist_atual = self.arena.distancia(robo, alvo)
            acao = robo.escolher_acao()

            if acao == "atacar":
                if dist_atual <= 1:
                    dano = robo.atacar(alvo)
                    self.logs.append(
                        f"{robo.nome} ATACA {alvo.nome} e causa {dano} de dano."
                    )
                else:
                    robo.mover_em_direcao(alvo, self.arena, aproximar=True)
                    nova_dist = self.arena.distancia(robo, alvo)
                    self.logs.append(
                        f"{robo.nome} se aproxima de {alvo.nome} "
                        f"para posição {robo.posicao()} (distância {nova_dist})."
                    )

            elif acao == "defender":
                self.logs.append(
                    f"{robo.nome} assume postura defensiva (ação ainda estética)."
                )

            elif acao == "esquivar":
                robo.mover_em_direcao(alvo, self.arena, aproximar=False)
                nova_dist = self.arena.distancia(robo, alvo)
                self.logs.append(
                    f"{robo.nome} tenta esquivar e recua para {robo.posicao()} "
                    f"(distância {nova_dist})."
                )

        # Checa fim de jogo
        if not self.jogador.esta_vivo() and not self.adversario.esta_vivo():
            # Empate teórico, mas vamos considerar derrota por enquanto
            self.status = "enemy_won"
            self.logs.append("Ambos os robôs caíram. Você perdeu (empate técnico).")
        elif not self.jogador.esta_vivo():
            self.status = "enemy_won"
            self.logs.append(f"{self.adversario.nome} venceu a batalha.")
        elif not self.adversario.esta_vivo():
            self.status = "player_won"
            self.logs.append(f"{self.jogador.nome} venceu a batalha.")

        self.turno += 1

    # -------------------------------
    # Helpers para serializar em JSON
    # -------------------------------

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "turno": self.turno,
            "jogador": self._robo_to_dict(self.jogador),
            "adversario": self._robo_to_dict(self.adversario),
            "logs": self.logs,
        }

    @staticmethod
    def _robo_to_dict(robo: Robo) -> dict:
        return {
            "nome": robo.nome,
            "cor": robo.cor,
            "ataque": robo.ataque,
            "defesa": robo.defesa,
            "velocidade": robo.velocidade,
            "hp_atual": robo.hp_atual,
            "hp_max": robo.hp_max,
            "x": robo.x,
            "y": robo.y,
        }
