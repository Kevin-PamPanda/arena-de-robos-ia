from __future__ import annotations

from fastapi.middleware.cors import CORSMiddleware


from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.models import Robo, Arena
from core.engine import GameState


app = FastAPI(title="ARIA - Arena de Robôs IA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Por enquanto vamos manter um único jogo em memória
current_game: Optional[GameState] = None


# -------------------------------
# Modelos de entrada/saída (Pydantic)
# -------------------------------


class NewGameRequest(BaseModel):
    robo_escolha: int  # 1 = vermelho, 2 = verde, 3 = azul
    nome: str


class CommandRequest(BaseModel):
    texto: str


class RoboOut(BaseModel):
    nome: str
    cor: str
    ataque: int
    defesa: int
    velocidade: int
    hp_atual: int
    hp_max: int
    x: int
    y: int


class GameStateOut(BaseModel):
    status: str
    turno: int
    jogador: RoboOut
    adversario: RoboOut
    logs: list[str]


def _game_to_out(game: GameState) -> GameStateOut:
    d = game.to_dict()
    return GameStateOut(
        status=d["status"],
        turno=d["turno"],
        jogador=RoboOut(**d["jogador"]),
        adversario=RoboOut(**d["adversario"]),
        logs=d["logs"],
    )


# -------------------------------
# Helpers para criar robôs
# -------------------------------


def criar_robo_inicial(escolha: int, nome: str) -> Robo:
    if escolha == 1:
        return Robo(nome, "vermelho", 3, 2, 1, "agressivo")
    elif escolha == 2:
        return Robo(nome, "verde", 2, 3, 1, "defensivo")
    elif escolha == 3:
        return Robo(nome, "azul", 1, 1, 4, "velocista")
    else:
        raise ValueError("Escolha de robô inválida. Use 1, 2 ou 3.")


def criar_robo_adversario_simples() -> Robo:
    # Versão simples: adversário fixo só pra testar a API
    return Robo("Adversário API", "branco", 2, 2, 2, "agressivo")


# -------------------------------
# Endpoints
# -------------------------------


@app.post("/new_game", response_model=GameStateOut)
def new_game(req: NewGameRequest):
    global current_game

    try:
        jogador = criar_robo_inicial(req.robo_escolha, req.nome)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    arena = Arena(largura=16, altura=5)
    adversario = criar_robo_adversario_simples()

    current_game = GameState(jogador=jogador, adversario=adversario, arena=arena)
    return _game_to_out(current_game)


@app.post("/command", response_model=GameStateOut)
def send_command(req: CommandRequest):
    if current_game is None:
        raise HTTPException(status_code=400, detail="Nenhum jogo ativo. Chame /new_game primeiro.")

    current_game.aplicar_comando(req.texto)
    return _game_to_out(current_game)


@app.post("/turno", response_model=GameStateOut)
def executar_turno():
    if current_game is None:
        raise HTTPException(status_code=400, detail="Nenhum jogo ativo. Chame /new_game primeiro.")

    current_game.executar_turno()
    return _game_to_out(current_game)


@app.get("/state", response_model=GameStateOut)
def get_state():
    if current_game is None:
        raise HTTPException(status_code=400, detail="Nenhum jogo ativo. Chame /new_game primeiro.")

    return _game_to_out(current_game)
